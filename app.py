from flask import Flask, render_template, request, redirect, url_for
import json
import re

app = Flask(__name__)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Pre-extract unique document names
documents = sorted(list(set(chunk["document"] for chunk in chunks_data)))

def get_answer(question, filtered_chunks):
    pattern = re.compile(re.escape(question), re.IGNORECASE)
    results = [chunk for chunk in filtered_chunks if pattern.search(chunk["content"])]
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    selected_doc = ""
    refine_query = ""
    answer = []

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_doc = request.form.get("document", "").strip()
        refine_query = request.form.get("refine_query", "").strip()

        if request.form.get("clear") == "1":
            return redirect(url_for("index"))

        filtered_chunks = chunks_data

        if selected_doc and selected_doc != "All Documents":
            filtered_chunks = [chunk for chunk in filtered_chunks if chunk["document"] == selected_doc]

        if refine_query:
            filtered_chunks = [chunk for chunk in filtered_chunks if refine_query.lower() in chunk["content"].lower()]

        if question:
            answer = get_answer(question, filtered_chunks)

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
