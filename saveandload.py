import os
import json
from datetime import datetime

SAVE_FOLDER = "saved_analysis"
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure the folder exists

def save_analysis(content, filename):
    """Save the analysis content as a JSON file with a given name."""
    if not content.strip():
        return {"error": "No content to save."}

    if not filename.endswith(".json"):
        filename += ".json"

    filepath = os.path.join(SAVE_FOLDER, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump({"content": content}, file, indent=4)
        return {"message": "Analysis saved successfully.", "filename": filename}
    except Exception as e:
        return {"error": str(e)}

def load_analysis():
    """Return a list of available saved analyses."""
    try:
        files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

def get_analysis_content(filename):
    """Load the content of a selected analysis file."""
    filepath = os.path.join(SAVE_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return {"error": "File not found."}

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return {"content": data.get("content", "No content found.")}
    except Exception as e:
        return {"error": str(e)}