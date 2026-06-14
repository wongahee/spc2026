from flask import Flask, request, jsonify, send_from_directory
import openai
import os
import sqlite3
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__, static_folder='static', static_url_path='')

conn = sqlite3.connect("conversations.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()

init_db()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customers",
            "description": "이름과 전화번호로 고객을 조회합니다. 없으면 새로 등록합니다. 예약/조회/삭제 전에 반드시 먼저 호출하세요.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "고객 이름"},
                    "phone": {"type": "string", "description": "고객 전화번호"}
                },
                "required": ["name", "phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": "예약을 생성합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "고객 ID"},
                    "date": {"type": "string", "description": "예약 날짜/시간 (예: 2026-06-20 14:00)"},
                    "note": {"type": "string", "description": "메모 (선택)"}
                },
                "required": ["customer_id", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointments",
            "description": "고객의 예약 목록을 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "고객 ID"}
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "예약을 취소합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "string", "description": "취소할 예약 ID (앞 8자리)"}
                },
                "required": ["appointment_id"]
            }
        }
    }
]

def execute_tool(name, args):
    if name == "get_customers":
        row = cursor.execute(
            "SELECT * FROM customers WHERE phone = ?", (args["phone"],)
        ).fetchone()
        if row:
            return f"기존 고객 확인: {row['name']} (ID: {row['id']})"
        new_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO customers (id, name, phone) VALUES (?, ?, ?)",
            (new_id, args["name"], args["phone"])
        )
        conn.commit()
        return f"신규 고객 등록: {args['name']} (ID: {new_id})"

    elif name == "create_appointment":
        new_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO appointments (id, customer_id, date, note) VALUES (?, ?, ?, ?)",
            (new_id, args["customer_id"], args["date"], args.get("note", ""))
        )
        conn.commit()
        return f"예약 완료! {args['date']} (예약 ID: {new_id[:8]})"

    elif name == "get_appointments":
        rows = cursor.execute(
            "SELECT * FROM appointments WHERE customer_id = ? ORDER BY date",
            (args["customer_id"],)
        ).fetchall()
        if not rows:
            return "예약 내역이 없습니다."
        return "\n".join([
            f"[{r['id'][:8]}] {r['date']} | {r['note']}"
            for r in rows
        ])

    elif name == "cancel_appointment":
        row = cursor.execute(
            "SELECT id FROM appointments WHERE id LIKE ?", (f"{args['appointment_id']}%",)
        ).fetchone()
        if not row:
            return "해당 예약을 찾을 수 없습니다."
        cursor.execute("DELETE FROM appointments WHERE id = ?", (row["id"],))
        conn.commit()
        return f"예약 {args['appointment_id']} 취소 완료"

    return "알 수 없는 도구입니다."


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    customer_id = data.get('customer_id', 'unknown')

    print("사용자 입력값: ", chat_message)

    cursor.execute(
        "INSERT INTO conversations (customer_id, role, content) VALUES (?, ?, ?)",
        (customer_id, 'user', chat_message)
    )
    conn.commit()

    gpt_reply = ask_chatgpt(customer_id)

    cursor.execute(
        "INSERT INTO conversations (customer_id, role, content) VALUES (?, ?, ?)",
        (customer_id, 'assistant', gpt_reply)
    )
    conn.commit()

    return jsonify({'reply': gpt_reply})

def ask_chatgpt(customer_id):
    rows = cursor.execute(
        "SELECT role, content FROM conversations WHERE customer_id = ? ORDER BY id ASC",
        (customer_id,)
    ).fetchall()

    messages = [{
        'role': 'system',
        'content': (
            '당신은 예약 상담 챗봇입니다. '
            '예약 생성/조회/삭제를 도와주세요. '
            '반드시 고객 이름과 전화번호를 먼저 확인한 뒤 예약을 진행하세요. '
            '날짜와 시간이 부족하면 친절하게 물어보세요.'
        )
    }]
    for row in rows:
        messages.append({'role': row['role'], 'content': row['content']})

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,
        tool_choice='auto'
    )
    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = execute_tool(tool_name, tool_args)
            print(f"도구 실행: {tool_name} → {tool_result}")
            messages.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': tool_result
            })
        second_response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        return second_response.choices[0].message.content

    return message.content

if __name__ == "__main__":
    app.run(debug=True)