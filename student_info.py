from flask import Blueprint, request, jsonify

student_bp = Blueprint("student", __name__)

# Mock students database (dictionary)
MOCK_STUDENTS = {
    "12345": {"name": "Anushka Mani Tripathi", "course": "B.S. Data Science and AI", "year": 3, "gpa": 8.9},
    "54321": {"name": "Aryan Rajput", "course": "B.Tech Computer Science", "year": 2, "gpa": 8.12},
    "11111": {"name": "Sundara Bharti", "course": "B.Sc Mathematics", "year": 1, "gpa": 9.01},
}

@student_bp.route("/student")
def get_student():
    # Example: /api/student?id=12345
    student_id = request.args.get("id", "").strip()
    if not student_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    student = MOCK_STUDENTS.get(student_id)
    if not student:
        return jsonify({"error": f"No student with id '{student_id}' found"}), 404

    response = {
        "id": student_id,
        "name": student["name"],
        "course": student["course"],
        "year": student["year"],
        "gpa": student["gpa"]
    }
    return jsonify(response)


@student_bp.route("/students/count")
def count_students():
    # Returns the number of students in the mock database
    total = len(MOCK_STUDENTS)
    return jsonify({"total_students": total})
