from flask import Flask, jsonify, request
from datetime import datetime

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

daily_tasks = [
    {
        "task": """ В честь тыквенного спаса дед Архип собрал 202500 тыкв, 
                    однако некоторые из них оказались испорченными. 
                    Архипу известно, что среди каждых 500 тыкв есть хотя бы одна порченая. 
                    Какое наибольшее количество хороших тыкв мог собрать Архип?""",
        "date": "17/02/2025",
        "solution": None,
        "image": "assets/meme.jpg"
    },
    {
        "task": """После учебы лицеисты разбегаются по своим домам, 
            каждый идет по кратчайшему расстоянию (по прямой от школы до дома). 
            Учитель географии узнал, что суммарное расстояние, 
            пройденное ими после школы на север равно расстоянию, 
            пройденному на юг, а также что расстояние, 
            пройденное на восток равно расстоянию, пройденному на запад. 
            Обязательно ли то же самое будет выполняться
             для северо востока и югозапада; северозапада и юговостока? 
             (считаем расстояние, пройденное в опр направлении как проекцию на прямую этого направления)""",
        "date": "17/02/2025",
        "solution": None,
        "image": None
    },
    {
        "task": """
        Найти точку, равноудалённую от четырёх точек
            Рассмотрим треугольник \\(ABC\\). Пусть:
            \\( I \\) — центр вписанной окружности треугольника \\( ABC \\).
            \\( I_a \\) — центр вневписанной окружности, противоположной вершине \\( A \\).
            \\( L \\) — точка пересечения отрезка \\( II_a \\) с дугой описанной окружности, не содержащей точку \\( A \\).
            Докажите, что точка \\( L \\) равноудалена от точек \\( I \\), \\( I_a \\), \\( B \\) и \\( C \\).
        """,
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


if __name__ == '__main__':
    app.run(debug=True)
