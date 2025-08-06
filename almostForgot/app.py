from flask import Flask, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)

TASKS_FILE = "tasks.csv"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task")
        recipient = request.form.get("recipient")
        timestamp = datetime.now().isoformat()
        
        if task and recipient:
            with open(TASKS_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([recipient, task.strip(), timestamp])
        return redirect("/")
    
    return'''
    <!doctype html>
    <html>
    <head>
        <title>Almost Forgot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: sans-serif;
                padding: 2rem;
                background-color: #fefae0;
                color: #fff;
                text-align: center;
            }
            input, select, button {
                padding: 1rem;
                margin: 0.5rem 0;
                width: 80%;
                font-size: 1rem;
            }
            button {
                background-color: #588157;
                color: white;
                border: none;
                cursor: pointer;
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
                <option  value="kaitie">Kaitie</option>
            </select><br>
            <button type="submit">Add Task</button>
        </form>
    </body>
    </html>
    '''
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
