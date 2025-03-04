import sqlite3

from flask import Flask, jsonify, request
from datetime import datetime

from flask_cors import CORS

conn = sqlite3.connect('tg_bot/users.db')
cursor = conn.cursor()

tasks_connection = sqlite3.connect('tasks.db')
tasks_cursor = tasks_connection.cursor()

tasks_cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   task TEXT NOT NULL, 
                   date TEXT NOT NULL,
                   solution TEXT,
                   image TEXT)''')

app = Flask(__name__)
CORS(app)


def get_daily_tasks():
    daily_tasks = tasks_cursor.execute('select * from tasks').fetchall()
    daily_tasks = [{"id": task[0], "task": task[1], "date": task[2], "solution": task[3], "image": task[4]} for task in
                   daily_tasks]
    return daily_tasks


def get_available_tasks():
    today = datetime.today()
    available_tasks = []

    for task in get_daily_tasks():
        task_date = datetime.strptime(task["date"], "%d/%m/%Y")
        if task_date <= today:
            available_tasks.append(task)
    available_tasks.sort(key=lambda t: datetime.strptime(t["date"], "%d/%m/%Y"), reverse=True)

    return available_tasks


@app.before_request
def add_cors_headers():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(get_available_tasks())


@app.route('/create-task', methods=['POST'])
def create_task():
    data = request.json
    tasks_cursor.execute("INSERT INTO tasks (task, date, solution, image) VALUES (?, ?, ?, ?)",
                         (data['task'], data['date'], data['image'], data['solution']))
    tasks_connection.commit()
    return jsonify({'status': 'OK'})


@app.route('/edit-task', methods=['POST'])
def edit_task():
    data = request.json
    return jsonify({'status': 'OK'})


@app.route('/delete-task', methods=['POST'])
def delete_task():
    data = request.json
    tasks_cursor.execute("DELETE FROM tasks WHERE id = ?", (data['task_id'],))
    tasks_connection.commit()
    return jsonify({'status': 'OK'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (data['username'],)).fetchone()
    return jsonify({'status': 'OK', 'user': user})


if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
