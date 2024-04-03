from flask import Flask, jsonify, request, abort
from datetime import datetime
from werkzeug.exceptions import BadRequest


app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List'


@app.route(BASE_URL + 'tasks', methods=['POST'])
def create_task():
    print("entreee")
    if not request.json:
        abort(404, error='Missing body in request')
    name = request.json.get('name')
    category = request.json.get('category')
    name_check = True
    category_check = True

    if not name:
        name_check = False
    if not category:
        category_check = False
    if not name or not category:
        return jsonify({'Name': name_check, 'Category': category_check}), 404


    this_time = datetime.now()
    task = {
        'id':len(tasks) + 1,
        'name' : request.json['name'],
        'category' : request.json['category'],
        'status' : False,
        'created' : this_time,
        'updated' : this_time
    }
    tasks.append(task)
    return jsonify({'Task': task}), 201 


@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    print("TASK")
    if len(this_task) == 0:
        abort(404, error= 'ID not found')
    return jsonify({'task': this_task[0]})

######################
@app.route("/tasks")

@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def check_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found')
    this_task[0]['status'] = not this_task[0]['status']

    return jsonify({'tasks': this_task[0]})

@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found')
    tasks.remove(this_task[0])
    return jsonify({'result':True })

    return jsonify({'tasks': this_task[0]})

if __name__ == "__main__":
    
    app.run(debug=True)
