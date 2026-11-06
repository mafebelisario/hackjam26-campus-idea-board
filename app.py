"""Campus Idea Board — Flask API and SQLite persistence."""
import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request

BASE = Path(__file__).resolve().parent
CATEGORIES = {"Best Overall", "Home Turf", "Off the Grid"}

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=str(BASE / "ideas.db"))
    if test_config:
        app.config.update(test_config)

    def connect():
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        return db

    def initialize():
        with connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                votes INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")

    initialize()

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/api/ideas")
    def get_ideas():
        # WORKSHOP STEP 3: retrieve saved ideas from SQLite.
        with connect() as db:
            rows = db.execute("SELECT * FROM ideas ORDER BY id DESC").fetchall()
        return jsonify([dict(row) for row in rows])

    @app.post("/api/ideas")
    def add_idea():
        # WORKSHOP STEP 2: validate incoming JSON and return a useful response.
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Send a JSON object."), 400
        title = data.get("title", "")
        description = data.get("description", "")
        category = data.get("category", "")
        if not isinstance(title, str) or not isinstance(description, str) or not isinstance(category, str):
            return jsonify(error="All fields must be text."), 400
        title, description = title.strip(), description.strip()
        if not (3 <= len(title) <= 100):
            return jsonify(error="Title must be 3–100 characters."), 400
        if not (5 <= len(description) <= 500):
            return jsonify(error="Description must be 5–500 characters."), 400
        if category not in CATEGORIES:
            return jsonify(error="Choose a valid category."), 400
        with connect() as db:
            cursor = db.execute("INSERT INTO ideas (title, description, category) VALUES (?, ?, ?)",
                                (title, description, category))
            row = db.execute("SELECT * FROM ideas WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201

    @app.post("/api/ideas/<int:idea_id>/upvote")
    def upvote(idea_id):
        # OPTIONAL STRETCH: one click adds one vote (no accounts/rate limiting).
        with connect() as db:
            cursor = db.execute("UPDATE ideas SET votes = votes + 1 WHERE id = ?", (idea_id,))
            if not cursor.rowcount:
                return jsonify(error="Idea not found."), 404
            row = db.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()
        return jsonify(dict(row))

    return app

if __name__ == "__main__":
    create_app().run(debug=True, host="127.0.0.1", port=5000)
