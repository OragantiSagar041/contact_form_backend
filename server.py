from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

# Allow GitHub Pages frontend
CORS(app, origins=["https://oragantisagar041.github.io"])

DB_NAME = "contacts.db"

# Initialize database
if not os.path.exists(DB_NAME):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    print("✅ Database initialized.")

# POST /contact → save form
@app.route("/contact", methods=["POST"])
def save_contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required"}), 400

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()

    return jsonify({"success": True, "message": "Contact saved successfully!"}), 201

# GET /contacts → list all
@app.route("/contacts", methods=["GET"])
def get_contacts():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC")
        rows = cursor.fetchall()

    contacts = [
        {"id": r[0], "name": r[1], "email": r[2], "message": r[3], "created_at": r[4]}
        for r in rows
    ]
    return jsonify(contacts)

if __name__ == "__main__":
    app.run(debug=True)
