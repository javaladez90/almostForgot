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



client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    client.messages.create(
        to=to,
        from_=TWILIO_FROM_NUMBER,
        body=message
    )
def ensure_schema():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            message TEXT NOT NULL,
            send_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def check_and_send_tasks():
    conn = sqlite3.connect("/data/tasks.db")
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec='minutes')

    cursor.execute("SELECT id, recipient, message, send_time FROM tasks")
    tasks = cursor.fetchall()

    for task in tasks:
        task_id, recipient, message, send_time = task

        if send_time <= now:
            phone_number = PHONE_NUMBERS.get(recipient.lower())
            if phone_number:
                print(f"Sending reminder to {recipient}: {message}")
                send_sms(phone_number, message)

                # Delete task after sending
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()

    conn.close()

if __name__ == "__main__":
    ensure_schema()
    check_and_send_tasks()
