from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

daily_tasks = [
    {
        "task": "В честь тыквенного спаса дед Архип собрал 202500 тыкв...",
        "date": "18/02/2025",
        "solution": None,
        "image": "assets/meme.jpg"
    },
    {
        "task": "После учебы лицеисты разбегаются по своим домам...",
        "date": "17/02/2025",
        "solution": None,
        "image": None
    },
    {
        "task": "Найти точку, равноудалённую от четырёх точек...",
        "date": "08/02/2025",
        "solution": "solution",
        "image": "assets/mansion-lemma.png"
    }
]


def get_available_tasks():
    today = datetime.today()
    available_tasks = []

    for task in daily_tasks:
        task_date = datetime.strptime(task["date"], "%d/%m/%Y")
        if task_date <= today:
            available_tasks.append(task)

    return available_tasks


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(get_available_tasks())

if __name__ == '__main__':
    app.run(debug=True)
