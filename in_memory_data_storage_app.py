from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory storage
tasks = []
categories = []

# Helper function to find overdue tasks
def is_overdue(due_date):
    if not due_date:
        return False
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        return due < datetime.now()
    except:
        return False

# Create a task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "completed": False,
        "category": data.get("category", None),
        "due_date": data.get("due_date", None),
        "priority": data.get("priority", "medium")
    }
    tasks.append(task)
    return jsonify(task), 201

# Get all tasks, optionally filter by category
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    category = request.args.get("category")
    filtered_tasks = [t for t in tasks if not category or t["category"] == category]
    return jsonify(filtered_tasks)

# Manage categories
@app.route("/api/categories", methods=["POST"])
def add_category():
    data = request.json
    category = data.get("name")
    if category and category not in categories:
        categories.append(category)
    return jsonify({"categories": categories})

# Get overdue tasks
@app.route("/api/tasks/overdue", methods=["GET"])
def get_overdue_tasks():
    overdue = [t for t in tasks if is_overdue(t.get("due_date"))]
    return jsonify(overdue)

@app.route("/api/tasks/stats", methods=["GET"])
def get_stats():
    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = total - completed
    overdue = len([t for t in tasks if is_overdue(t.get("due_date"))])
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    })
