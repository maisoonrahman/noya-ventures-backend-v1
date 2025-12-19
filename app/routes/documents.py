import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400
    
    filename = secure_filename(file.filename)
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"message": "Uploaded", "filename": filename}), 201