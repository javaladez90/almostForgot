from flask import Flask, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = "/data/tasks.db"

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

@app.route("/", methods=["GET", "POST"])
def home():
    ensure_schema()

    if request.method == "POST":
        message   = request.form["task"].strip()
        recipient = request.form["recipient"].strip()
        send_time = request.form["send_time"].strip()

        conn   = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (recipient, message, send_time) VALUES (?,?,?)",
            (recipient, message, send_time)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    # GET falls through to render the HTML form
    return '''
    <!doctype html>
    <html>
    <head> … your <style> … </head>
    <body>
      <h1>Almost Forgot</h1>
      <form method="post">
        <input type="text" name="task" placeholder="What do you need to remember?" required><br>
        <select name="recipient" required>
          <option value="" disabled selected>Send reminder to…</option>
          <option value="jose">Jose</option>
          <option value="wife">Wife</option>
        </select><br>
        <input type="datetime-local" id="taskTime" name="send_time" required><br>
        <button type="submit">Add Task</button>
      </form>
      <script>
        window.onload = () => {
          const now = new Date();
          now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
          document.getElementById('taskTime').value = now.toISOString().slice(0,16);
        };
      </script>
    </body>
    </html>
    '''

@app.route("/debug/tasks")
def debug_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, recipient, message, send_time FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
      {"id": r[0], "recipient": r[1], "message": r[2], "send_time": r[3]}
      for r in rows
    ]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
