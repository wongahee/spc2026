from flask import Flask, request, jsonify, send_from_directory
import openai
import os
import uuid
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

# 환경 변수 로드
load_dotenv()

# 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__, static_folder='static', static_url_path='')

# ERD 구조상 상위 개념인 가상의 비즈니스 ID (가게 ID)
MOCK_BUSINESS_ID = "b1111111-1111-1111-1111-111111111111"
# 웹 채팅 테스트를 위한 고정 사용자 ID (로그인 기능이 없는 MVP 단계용)
TEMPORARY_CUSTOMER_ID = "c9999999-9999-9999-9999-999999999999"


# ==========================================
# AI Agent가 인식할 도구(Tools) 정의
# ==========================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": "고객의 예약을 생성하여 데이터베이스에 등록합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "고객 이름"},
                    "date": {"type": "string", "description": "예약 날짜 (예: 2026-06-20)"},
                    "time": {"type": "string", "description": "예약 시간 (예: 14:00)"},
                    "note": {"type": "string", "description": "추가 요구사항 메모 (선택)"}
                },
                "required": ["customer_name", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointments",
            "description": "고객 이름을 기반으로 예약 목록을 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "조회할 고객 이름 (선택)"}
                }
            }
        }
    }
]


# ==========================================
# Supabase 제어 비즈니스 로직 (Tools 실행 함수)
# ==========================================
def execute_tool(name, args):
    if name == "create_appointment":
        customer_name = args["customer_name"]
        
        # 1. Customers 테이블에서 해당 이름을 가진 고객 조회
        customer_res = supabase.table("customers").select("id").eq("name", customer_name).execute()
        customers = customer_res.data
        
        if customers:
            customer_id = customers[0]["id"]
        else:
            # 존재하지 않는 회원이라면 새로 생성 (ERD 규칙 준수)
            customer_id = str(uuid.uuid4())
            supabase.table("customers").insert({
                "id": customer_id,
                "business_id": MOCK_BUSINESS_ID,
                "name": customer_name
            }).execute()
        
        # 2. 날짜 및 시간 포맷팅 (시작 시간과 1시간 뒤 종료 시간 설정)
        start_time_str = f"{args['date']} {args['time']}:00"
        start_dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_dt = start_dt + timedelta(hours=1)
        
        # 3. Appointments 테이블에 최종 예약 정보 기입
        appointment_id = str(uuid.uuid4())
        supabase.table("appointments").insert({
            "id": appointment_id,
            "business_id": MOCK_BUSINESS_ID,
            "customer_id": customer_id,
            "status": "확정",
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "note": args.get("note", "")
        }).execute()
        
        return f"{customer_name}님 {args['date']} {args['time']} 예약이 완료되었습니다."

    elif name == "get_appointments":
        name_filter = args.get("customer_name")
        
        if name_filter:
            # 먼저 이름으로 고객 ID를 찾음
            customer_res = supabase.table("customers").select("id").ilike("name", f"%{name_filter}%").execute()
            customer_ids = [c["id"] for c in customer_res.data]
            
            if not customer_ids:
                return f"{name_filter} 고객님 명의의 예약 내역이 없습니다."
                
            # 해당 고객 ID 목록에 매칭되는 예약 조회
            app_res = supabase.table("appointments").select("*").in_("customer_id", customer_ids).execute()
            rows = app_res.data
        else:
            # 전체 조회
            app_res = supabase.table("appointments").select("*").execute()
            rows = app_res.data

        if not rows:
            return "등록된 예약 내역이 없습니다."
            
        # 간단히 텍스트로 가공해서 GPT에게 반환
        result_lines = []
        for r in rows:
            # 가독성을 위해 이름 매칭용 역조회 (생략 가능)
            c_res = supabase.table("customers").select("name").eq("id", r["customer_id"]).execute()
            c_name = c_res.data[0]["name"] if c_res.data else "알 수 없음"
            result_lines.append(f"고객: {c_name} | 일정: {r['start_time']} ~ {r['end_time']} | 상태: {r['status']}")
            
        return "\n".join(result_lines)

    return "알 수 없는 도구입니다."


# ==========================================
# Flask 라우터 및 API 엔드포인트
# ==========================================
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    
    # 셈플 유저가 없으면 에러방지용 자동 가입
    user_check = supabase.table("customers").select("id").eq("id", TEMPORARY_CUSTOMER_ID).execute()
    if not user_check.data:
        supabase.table("customers").insert({
            "id": TEMPORARY_CUSTOMER_ID,
            "business_id": MOCK_BUSINESS_ID,
            "name": "기본 테스트 유저"
        }).execute()

    # 1. 유저가 보낸 메시지 Supabase 'conversations' 테이블에 기록 (channel='user')
    supabase.table("conversations").insert({
        "id": str(uuid.uuid4()),
        "business_id": MOCK_BUSINESS_ID,
        "customer_id": TEMPORARY_CUSTOMER_ID,
        "channel": "user",
        "message": chat_message
    }).execute()

    # 2. GPT 답변 생성 로직 실행
    gpt_reply = ask_chatgpt()

    # 3. GPT가 생성한 답변을 'conversations' 테이블에 기록 (channel='assistant')
    supabase.table("conversations").insert({
        "id": str(uuid.uuid4()),
        "business_id": MOCK_BUSINESS_ID,
        "customer_id": TEMPORARY_CUSTOMER_ID,
        "channel": "assistant",
        "message": gpt_reply
    }).execute()

    return jsonify({ 'reply': gpt_reply })


def ask_chatgpt():
    # Supabase에서 전체 대화 히스토리 역순으로 가져오기
    history_res = supabase.table("conversations") \
                          .select("channel", "message") \
                          .eq("customer_id", TEMPORARY_CUSTOMER_ID) \
                          .order("created_at", ascending=True) \
                          .execute()
    rows = history_res.data

    messages = [
        {
            'role': 'system',
            'content': '당신은 예약 상담 챗봇입니다. 고객의 예약 생성 및 조회를 도와주세요. 날짜나 시간이 불명확하면 다시 물어보세요.'
        }
    ]

    # 불러온 DB 내용을 OpenAI 규격('role', 'content')으로 변경해서 빌드
    for row in rows:
        messages.append({
            'role': row['channel'], # 'user' 혹은 'assistant'
            'content': row['message']
        })

    # OpenAI 컴플리션 호출 (1차)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,
        tool_choice='auto'
    )

    message = response.choices[0].message

    # AI가 도구 실행(함수 호출)을 선언한 경우
    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            # 실제 Supabase를 수정하는 파이썬 함수 연동
            tool_result = execute_tool(tool_name, tool_args)

            messages.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': tool_result
            })

        # 도구 실행 결과를 취합해서 최종 자연어 문장 생성 (2차)
        second_response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        return second_response.choices[0].message.content
    
    return message.content


if __name__ == "__main__":
    app.run(debug=True, port=5000)