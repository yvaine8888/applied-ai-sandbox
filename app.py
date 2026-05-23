"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        query = (request.args.get("q") or "").strip()
        if query:
            search_term = query.lower()
            filtered_notes = [
                note for note in app.notes
                if search_term in note["title"].lower() or search_term in note["body"].lower()
            ]
        else:
            filtered_notes = app.notes
        return render_template("home.html", notes=filtered_notes, q=query)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            tags_raw = request.form.get("tags") or ""
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
            title_error = "Title is required" if not title else None
            body_error = "Body is required" if not body else None
            if title_error or body_error:
                return render_template(
                    "new_note.html",
                    title=title,
                    body=body,
                    title_error=title_error,
                    body_error=body_error,
                )
            app.notes.append({"title": title, "body": body, "tags": tags})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
