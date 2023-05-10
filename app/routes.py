from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort

task_list_bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")

def validate_model_task(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return task

@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.task_from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.task_to_dict()
    }
    return response_body, 201

@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.task_to_dict())

    return jsonify(tasks_response)

@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model_task(Task, task_id)
    response_body = {
        "task": task.task_to_dict()
    }
    return jsonify(response_body)

@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model_task(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]

    db.session.commit()

    response_body = {
        "task": task.task_to_dict()
    }
    return response_body

@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model_task(Task, task_id)
    response_body = {
        "details": f"Task {task.task_id} \{task.title}\ succussfully deleted"
    }

    db.session.delete(task)
    db.session.commit()

    return response_body
