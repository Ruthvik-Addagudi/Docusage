from flask import Flask, request, jsonify, render_template, send_file
import os
from modules.summarization import summarize_text  # Ensure this module exists and works as expected
from modules.text_extraction import extract_text_with_PyMuPDF  # Import PDF text extraction
from modules.true_false_generator import generate_true_false_questions
from modules.fill_in_the_blanks_generator import generate_fill_in_the_blanks
from modules.mind_map_generation import create_mind_map_from_text
from modules.search import search_bp  # Import the new module
from modules.dqa_module import generate_feedback_report

app = Flask(__name__)

# Store last evaluation for feedback download
last_feedback = []
last_score = 0
last_total = 0

#from flask_cors import CORS
import json
#print("Importing mcq_generator...")
from modules.mcq_generator import generate_mcqs
#print("mcq_generator imported successfully.")


app = Flask(__name__)
#CORS(app)

app.register_blueprint(search_bp)  # Register the Blueprint

SAVE_DIR = "saved_analysis" 
os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure the folder exists

# Configure the uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """Serve the main UI."""
    return render_template('index.html')  # Ensure index.html is in the templates/ folder

import re

# Store extracted text globally to avoid repeated extractions
extracted_text_cache = ""

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and extract text once."""
    global extracted_text_cache
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text and store in cache
        extracted_text_cache = extract_text_with_PyMuPDF(file_path)
        
        return jsonify({'message': f'File uploaded successfully: {file.filename}', 'file_path': file_path})

    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

@app.route('/search', methods=['POST'])
def search_text():
    """Search for a keyword in the extracted PDF text."""
    global extracted_text_cache
    data = request.json
    keyword = data.get('keyword', '').strip()

    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400
    if not extracted_text_cache:
        return jsonify({'error': 'No text available. Upload a PDF first.'}), 400

    # Find matches and their surrounding context
    matches = []
    pattern = re.compile(rf"(.{{0,50}}{re.escape(keyword)}.{{0,50}})", re.IGNORECASE)
    for match in pattern.findall(extracted_text_cache):
        matches.append(match.replace(keyword, f"<mark>{keyword}</mark>"))  # Highlight the keyword

    return jsonify({'results': matches})


@app.route('/summarize', methods=['POST'])
def summarize():
    """Handle summarization requests."""
    try:
        # Get the text input from the POST request
        data = request.json
        text = data.get('text', '')

        if not text.strip():
            return jsonify({'error': 'No text provided for summarization'}), 400

        # Call the summarization function
        summary = summarize_text(text, max_length=100, min_length=30)
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/extract-text', methods=['POST'])
def extract_text():
    """Handle text extraction from the uploaded PDF."""
    try:
        data = request.json
        file_path = data.get('file_path', '')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        
        # Extract text from the PDF using PyMuPDF
        text = extract_text_with_PyMuPDF(file_path)
        if not text.strip():
            return jsonify({'error': 'No text extracted from PDF'}), 400
        
        return jsonify({'text': text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Global variables to store generated question sets
true_false_data = []
fill_in_the_blanks_data = []
mcq_data = []
    
@app.route('/true-false', methods=['POST'])
def generate_true_false():
    """Generate true/false questions from the provided text."""
    global true_false_data  # <-- use global variable
    
    try:
        data = request.json
        text = data.get('text', '')  # Get the input text from the POST request
        num_questions = data.get('num_questions', 5)  # Default to 5 questions if not provided
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate true/false questions
        questions = generate_true_false_questions(text, num_questions)
        
        # Format the response
        true_false_data = [{'question': q, 'answer': a} for q, a in questions]  # <-- store globally
        return jsonify({'questions': true_false_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/fill-in-the-blanks', methods=['POST'])
def fill_in_the_blanks():
    global fill_in_the_blanks_data  # <-- use global variable

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request. 'text' is required."}), 400
    
    text = data['text']
    num_questions = data.get('num_questions', 3)  # Default to 3 questions if not specified
    
    try:
        questions = generate_fill_in_the_blanks(text, num_questions=num_questions)
        fill_in_the_blanks_data = [{"question": q[0], "answer": q[1]} for q in questions]  # <-- store globally
        return jsonify({"questions": fill_in_the_blanks_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/mcq', methods=['POST'])
def generate_mcq():
    """Generate multiple-choice questions (MCQs) from the provided text."""
    global mcq_data  # <-- use global variable

    try:
        data = request.json
        text = data.get('text', '')  # Get the input text from the POST request
        num_questions = data.get('num_questions', 5)  # Default to 5 questions if not provided

        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400

        # Generate MCQs
        questions = generate_mcqs(text, num_questions)

        # Format the response
        mcq_data = [{
            'question': q['question'],
            'options': q['options'],
            'correct_answer': q['correct_answer']
        } for q in questions]  # <-- store globally
        
        return jsonify({'mcqs': mcq_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/generate-mind-map', methods=['POST'])
def generate_mind_map():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided."}), 400

    try:
        # Call the mind map generation function
        create_mind_map_from_text(text)

        return jsonify({"message": "Mind map generated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Download the analysis file
@app.route("/download", methods=["GET"])
def download_analysis():
    if not os.path.exists(SINGLE_SAVE_FILE): # type: ignore
        return jsonify({"error": "No analysis file found."}), 404
    return send_file(SINGLE_SAVE_FILE, as_attachment=True, download_name="saved_analysis.json") # type: ignore

@app.route('/save', methods=['POST'])
def save_analysis():
    data = request.json
    file_name = data.get("fileName", "default_analysis.json").strip()

    if not file_name.endswith(".json"):
        file_name += ".json"

    file_path = os.path.join(SAVE_DIR, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"content": data["content"]}, file, ensure_ascii=False, indent=4)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/load', methods=['GET'])
def list_saved_analyses():
    try:
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_analysis', methods=['GET'])
def get_analysis():
    file_name = request.args.get("file")
    file_path = os.path.join(SAVE_DIR, file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/delete', methods=['DELETE'])
def delete_analysis():
    file_name = request.args.get("file")
    file_path = os.path.join(SAVE_DIR, file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        os.remove(file_path)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Dynamic Question Generation and Evaluation

@app.route("/generate_dqa", methods=["POST"])
def generate_dqa():
    try:
        print("📡 Received request at /generate_dqa")
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request, no JSON data received"}), 400

        question_types = data.get("question_types", [])
        num_questions = int(data.get("num_questions", 5))

        if not question_types:
            return jsonify({"error": "No question types selected"}), 400

        selected_questions = []

        if "mcq" in question_types:
            if not mcq_data:
                return jsonify({"error": "MCQ questions not generated yet"}), 400
            selected_questions.extend(mcq_data[:num_questions])

        if "true_false" in question_types:
            if not true_false_data:
                return jsonify({"error": "True/False questions not generated yet"}), 400
            selected_questions.extend(true_false_data[:num_questions])

        if "fill_in_the_blanks" in question_types:
            if not fill_in_the_blanks_data:
                return jsonify({"error": "Fill in the Blanks questions not generated yet"}), 400
            selected_questions.extend(fill_in_the_blanks_data[:num_questions])

        # Final slice if too many questions added
        selected_questions = selected_questions[:num_questions]

        print("✅ Questions sent:", selected_questions)
        return jsonify({"questions": selected_questions})

    except Exception as e:
        print(f"❌ ERROR in /generate_dqa: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/evaluate_dqa', methods=['POST'])
def evaluate_dqa():
    global last_feedback, last_score, last_total  # Add this line

    data = request.json
    user_answers = data.get("answers", [])

    score = 0
    feedback = []

    for question in user_answers:
        correct_answer = question["correct_answer"]
        user_answer = question["user_answer"]

        if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
            score += 1
            feedback.append({"question": question["question"], "correct": True})
        else:
            feedback.append({
                "question": question["question"],
                "correct": False,
                "correct_answer": correct_answer
            })

    # ✅ Store in global vars
    last_feedback = feedback
    last_score = score
    last_total = len(user_answers)

    return jsonify({"score": score, "total": last_total, "feedback": feedback})

 
@app.route('/download_feedback')
def download_feedback():
    """
    Allows downloading feedback as a file.
    """
    global last_feedback, last_score, last_total

    if not last_feedback:
        return jsonify({"error": "No feedback available"}), 400

    file_path = generate_feedback_report(last_feedback, last_score, last_total)

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=False)