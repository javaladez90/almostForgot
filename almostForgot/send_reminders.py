import sqlite3
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

# Phone numbers mapping
PHONE_NUMBERS = {
    "jose": os.getenv("PHONE_JOSE"),
    "wife": os.getenv("PHONE_WIFE")
}

# Database path, fallback to local tasks.db in CI
DB_PATH = os.getenv("TASKS_DB_PATH", "tasks.db")

# Twilio client setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, message):
    """Send SMS via Twilio."""
    client.messages.create(
        to=to,
        from_=TWILIO_FROM_NUMBER,
        body=message
    )


def ensure_schema():
    """Create tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            message TEXT NOT NULL,
            send_time TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def check_and_send_tasks():
    """Fetch due tasks, send SMS, and delete them."""
    ensure_schema()
    now = datetime.now()
    print(f"[DEBUG] runner now = {now.isoformat(timespec='minutes')}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, recipient, message, send_time FROM tasks")
    tasks = cursor.fetchall()

    for task_id, recipient, message, send_time_str in tasks:
        try:
            send_dt = datetime.fromisoformat(send_time_str)
        except ValueError as e:
            print(f"[DEBUG] could not parse send_time='{send_time_str}': {e}")
            continue

        print(f"[DEBUG] task={task_id} recipient={recipient} send_time_str={send_time_str} parsed={send_dt.isoformat(timespec='minutes')}")

        if send_dt <= now:
            print(f"Sending reminder to {recipient}: {message}")
            send_sms(PHONE_NUMBERS.get(recipient, ""), message)
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    conn.close()


if __name__ == "__main__":
    check_and_send_tasks()
