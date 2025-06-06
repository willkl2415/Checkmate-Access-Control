# app.py

import os
from flask import Flask, render_template, request, redirect, url_for
import json
from answer_engine import get_answer

app = Flask(__name__)

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
    question = ""
    selected_doc = ""
    refine_query = ""
    answer = []

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        refine_query = request.form.get("refine_query", "")

        if request.form.get("clear") == "1":
            return redirect(url_for("index"))

        filtered_chunks = chunks_data
        if selected_doc and selected_doc != "All Documents":
            filtered_chunks = [chunk for chunk in filtered_chunks if chunk["document"] == selected_doc]

        if refine_query:
            filtered_chunks = [chunk for chunk in filtered_chunks if refine_query.lower() in chunk["content"].lower()]

        answer = get_answer(question, filtered_chunks) if question else []

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=["All Documents"] + documents,
        selected_doc=selected_doc,
        refine_query=refine_query
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
