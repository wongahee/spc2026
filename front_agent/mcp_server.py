from mcp.server import Server
from mcp.server.stdio import stdio_server
import sqlite3
import uuid
import asyncio

app = Server("appointment-server")

conn = sqlite3.connect("conversations.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


@app.tool()
async def get_or_create_customer(phone: str, name: str):
    """전화번호로 고객 조회. 없으면 신규 등록."""
    row = cursor.execute(
        "SELECT * FROM customers WHERE phone = ?", (phone,)
    ).fetchone()

    if row:
        return {"status": "found", "customer_id": row["id"], "name": row["name"], "phone": row["phone"]}

    new_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO customers (id, name, phone) VALUES (?, ?, ?)",
        (new_id, name, phone)
    )
    conn.commit()
    return {"status": "created", "customer_id": new_id, "name": name, "phone": phone}


@app.tool()
async def create_appointment(customer_id: str, date: str, note: str = ""):
    """예약 생성"""
    new_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO appointments (id, customer_id, date, note) VALUES (?, ?, ?, ?)",
        (new_id, customer_id, date, note)
    )
    conn.commit()
    return {"status": "success", "appointment_id": new_id[:8], "date": date}


@app.tool()
async def get_appointments(customer_id: str):
    """예약 조회"""
    rows = cursor.execute(
        "SELECT * FROM appointments WHERE customer_id = ? ORDER BY date",
        (customer_id,)
    ).fetchall()

    if not rows:
        return []
    return [{"appointment_id": r["id"][:8], "date": r["date"], "note": r["note"]} for r in rows]


@app.tool()
async def delete_appointment(appointment_id: str):
    """예약 삭제"""
    row = cursor.execute(
        "SELECT id FROM appointments WHERE id LIKE ?", (f"{appointment_id}%",)
    ).fetchone()

    if not row:
        return {"status": "error", "message": "예약을 찾을 수 없습니다."}

    cursor.execute("DELETE FROM appointments WHERE id = ?", (row["id"],))
    conn.commit()
    return {"status": "success", "appointment_id": appointment_id}


if __name__ == "__main__":
    asyncio.run(stdio_server(app))