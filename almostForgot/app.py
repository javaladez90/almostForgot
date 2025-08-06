from flask import Flask, request, redirect

import sqlite3
from datetime import datetime



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form.get("task")
        recipient = request.form.get("recipient")
        send_time = request.form.get("send_time")  # format: YYYY-MM-DDTHH:MM

        if message and recipient and send_time:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (recipient, message, send_time) VALUES (?, ?, ?)",
                (recipient.strip(), message.strip(), send_time.strip())
            )
            conn.commit()
            conn.close()
            return redirect("/")

    return '''
    <!doctype html>
    <html>
    <head>
        <title>Almost Forgot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                box-sizing: border-box;
            }
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
                h1 {
                    font-size: 1.6rem;
                }
                form {
                    padding: 1.5rem;
                }
                button {
                    font-size: 0.95rem;
                }
            }
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
            window.onload = function () {
                const now = new Date();
                now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
                document.getElementById('taskTime').value = now.toISOString().slice(0, 16);
            };
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
