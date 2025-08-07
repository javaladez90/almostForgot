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

    # GET → render the form
    return '''
    <!doctype html>
    <html>
      <head>
        <title>Almost Forgot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          <style>
  * { box-sizing: border-box; }

  body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f7f7f7;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    flex-direction: column;
  }

  h1 {
    margin-bottom: 1rem;
    font-size: 2rem;
    color: #2c3e50;
    text-align: center;
  }

  form {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    width: 90%;
    max-width: 400px;
    text-align: center;
  }

  input[type="text"],
  input[type="datetime-local"],
  select {
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 6px;
  }

  button {
    width: 100%;
    padding: 1rem;
    background-color: #3d8361;
    color: white;
    border: none;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }

  button:hover {
    background-color: #2b644b;
  }

  @media (max-width: 480px) {
    h1 { font-size: 1.6rem; }
    form { padding: 1.5rem; }
    button { font-size: 0.95rem; }
  }
</style>

        </style>
      </head>
      <body>
        <h1>Almost Forgot</h1>
        <form method="post">
          <input type="text" name="task" placeholder="What do you need to remember?" required><br>
          <select name="recipient" required>
            <option value="" disabled selected>Send reminder to...</option>
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
