# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from answer_engine import get_answer
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "change_this_to_something_secure"
app.register_blueprint(auth_bp)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks_data))
document_sections = {}
for chunk in chunks_data:
    doc = chunk["document"]
    section = chunk.get("section", "Uncategorised")
    if doc not in document_sections:
        document_sections[doc] = set()
    document_sections[doc].add(section)

@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    question = request.form.get("question", "")
    selected_doc = request.form.get("document", "")
    refine_query = request.form.get("refine_query", "")

    if request.form.get("clear") == "1":
        return redirect(url_for("index"))

    filtered_chunks = chunks_data
    if selected_doc:
        filtered_chunks = [chunk for chunk in filtered_chunks if chunk["document"] == selected_doc]

    if refine_query:
        filtered_chunks = [chunk for chunk in filtered_chunks if refine_query.lower() in chunk["content"].lower()]

    answer = get_answer(question, filtered_chunks) if question else []

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        selected_doc=selected_doc,
        refine_query=refine_query
    )

if __name__ == "__main__":
    app.run(debug=True)
