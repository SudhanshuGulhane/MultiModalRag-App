from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from multimodalrag.data_retrieval import *
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chatbot():  
    input_text = request.form.get("msg")
    uploaded_file = request.files.get("file")

    print('input ', input_text)

    file_path = None

    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)