from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Path to your chunks.json file
CHUNKS_PATH = os.path.join("data", "chunks.json")

# Load chunks from file
chunks = []
documents = []
refine_options = []
error_message = ""

try:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        documents = sorted(set(chunk.get("document", "Unknown") for chunk in chunks))
        refine_options = sorted(set(chunk.get("section", "Uncategorised") for chunk in chunks if chunk.get("section")))
except FileNotFoundError:
    error_message = f"ERROR: Could not find {CHUNKS_PATH}"
except json.JSONDecodeError:
    error_message = f"ERROR: {CHUNKS_PATH} is not valid JSON"
except Exception as e:
    error_message = f"UNEXPECTED ERROR: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = []
    selected_doc = "All Documents"
    selected_section = "All Sections"

    if request.method == "POST":
        if request.form.get("clear") == "1":
            return render_template("index.html",
                                   question="",
                                   answer=[],
                                   documents=documents,
                                   refine_options=refine_options,
                                   selected_doc="All Documents",
                                   selected_section="All Sections",
                                   error=error_message)

        question = request.form.get("question", "").strip().lower()
        selected_doc = request.form.get("document", "All Documents")
        selected_section = request.form.get("refine", "All Sections")

        for chunk in chunks:
            content = chunk.get("content", "").lower()
            if question in content:
                if selected_doc != "All Documents" and chunk.get("document") != selected_doc:
                    continue
                if selected_section != "All Sections" and chunk.get("section") != selected_section:
                    continue
                answer.append(chunk)

    return render_template("index.html",
                           question=question,
                           answer=answer,
                           documents=documents,
                           refine_options=refine_options,
                           selected_doc=selected_doc,
                           selected_section=selected_section,
                           error=error_message)


if __name__ == "__main__":
    app.run(debug=True)
