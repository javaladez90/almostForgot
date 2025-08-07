import sqlite3
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
import os


load_dotenv()


# Grab them from the environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")



PHONE_NUMBERS = {
    "jose": os.getenv("PHONE_JOSE"),
    "wife": os.getenv("PHONE_WIFE")
}


DB_PATH = os.getenv("TASKS_DB_PATH", "tasks.db")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    client.messages.create(
        to=to,
        from_=TWILIO_FROM_NUMBER,
        body=message
    )
    
def ensure_schema():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient TEXT NOT NULL,
        message TEXT NOT NULL,
        send_time TEXT NOT NULL
      )
    """)
    conn.commit()
    conn.close()

from datetime import datetime

def check_and_send_tasks():
    now = datetime.now()
    print(f"[DEBUG] runner now = {now.isoformat(timespec='minutes')}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, recipient, message, send_time FROM tasks")
    tasks = cursor.fetchall()

    for task_id, recipient, message, send_time_str in tasks:
        # parse the stored ISO string (no timezone info)
        send_dt = datetime.fromisoformat(send_time_str)
        print(f"[DEBUG] task {task_id} send_time = {send_dt.isoformat(timespec='minutes')}")

        if send_dt <= now:
            print(f"Sending reminder to {recipient}: {message}")
            send_sms(PHONE_NUMBERS[recipient], message)
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
    conn.close()


if __name__ == "__main__":
    ensure_schema()
    check_and_send_tasks()
