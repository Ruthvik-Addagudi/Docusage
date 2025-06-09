import os
import json
from flask import Blueprint, request, jsonify

# Create a Blueprint for search-related functions
search_bp = Blueprint("search", __name__)

# Directory where saved analyses will be stored
SAVE_DIR = "saved_analysis"

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

@search_bp.route("/save_analysis", methods=["POST"])
def save_analysis():
    """Saves the current analysis as a JSON file."""
    data = request.json
    content = data.get("content", "")
    filename = data.get("filename", "")

    if not content:
        return jsonify({"error": "No content to save"}), 400

    # Default filename if not provided
    if not filename:
        filename = f"analysis_{len(os.listdir(SAVE_DIR)) + 1}.json"

    file_path = os.path.join(SAVE_DIR, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"content": content}, f, ensure_ascii=False, indent=4)
        return jsonify({"message": "Analysis saved successfully!", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@search_bp.route("/load_analysis", methods=["GET"])
def load_analysis():
    """Returns a list of saved analysis files."""
    try:
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@search_bp.route("/get_analysis", methods=["POST"])
def get_analysis():
    """Loads the content of a selected analysis file."""
    data = request.json
    filename = data.get("filename", "")

    if not filename:
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(SAVE_DIR, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500