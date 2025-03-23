from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from multimodalrag.data_loading_processing import *
from multimodalrag.data_transformation import *
from multimodalrag.data_storing import *
from multimodalrag.data_retrieval import *

import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

retriever_cache = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")
    
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    filename, _ = os.path.splitext(uploaded_file.filename)

    texts_data, tables_data, images_data = load_document(file_path)
    text_summaries = summarize_text(texts_data)
    table_summaries = summarize_tables(tables_data)
    image_summaries = summarize_images(images_data)

    retriever = create_multimodal_retriever(
        filename,
        text_summaries, texts_data,
        table_summaries, tables_data,
        image_summaries, images_data
    )
    retriever_cache[filename] = rag_chain_for_multi_modal(retriever)

    return jsonify({"message": "File uploaded successfully", "filename": uploaded_file.filename})

@app.route("/query", methods=["POST"])
def query_file():
    data = request.get_json()
    query = data.get("query")
    file = data.get("filename")

    filename, _ = os.path.splitext(file)

    if not query or not filename:
        return jsonify({"error": "Missing query or filename"}), 400

    if filename not in retriever_cache:
        return jsonify({"error": "File not uploaded or retriever not found"}), 404

    chain = retriever_cache[filename]
    response = chain.invoke(query)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
