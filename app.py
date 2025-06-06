# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from answer_engine import get_answer
from auth import auth_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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

document_sections = {doc: sorted(sections) for doc, sections in document_sections.items()}

@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    question = ""
    selected_doc = ""
    selected_section = ""
    refine_query = ""
    answer = []

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        selected_section = request.form.get("section", "")
        refine_query = request.form.get("refine_query", "")

        if request.form.get("clear") == "1":
            return redirect(url_for("index"))

        filtered_chunks = chunks_data

        if selected_doc and selected_doc != "All Documents":
            filtered_chunks = [chunk for chunk in filtered_chunks if chunk["document"] == selected_doc]

        if selected_section and selected_section != "All Sections":
            filtered_chunks = [chunk for chunk in filtered_chunks if chunk.get("section") == selected_section]

        if refine_query:
            filtered_chunks = [chunk for chunk in filtered_chunks if refine_query.lower() in chunk["content"].lower()]

        if question:
            answer = get_answer(question, filtered_chunks)

    return render_template(
        "index.html",
        documents=["All Documents"] + documents,
        selected_doc=selected_doc,
        document_sections=document_sections,
        selected_section=selected_section,
        question=question,
        refine_query=refine_query,
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)
