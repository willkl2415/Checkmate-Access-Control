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
