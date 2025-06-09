import requests # type: ignore
import json

DQA_API_URL = "http://localhost:5000/generate_dqa"
EVALUATE_API_URL = "http://localhost:5000/evaluate_dqa"
FEEDBACK_FILE = "feedback_report.txt"


def start_dqa_quiz(question_types, num_questions):
    """
    Starts the DQA quiz by fetching pre-generated questions of selected types.
    """

    payload = {
        "question_types": question_types,
        "num_questions": num_questions
    }

    response = requests.post(DQA_API_URL, json=payload)

    if response.status_code != 200:
        print(f"❌ Failed to generate questions: {response.json().get('error')}")
        return

    questions = response.json().get("questions", [])
    user_answers = []

    print("\n📋 Starting Quiz...\n")

    for idx, q in enumerate(questions, 1):
        print(f"Q{idx}: {q['question']}")

        if "options" in q:  # MCQ
            for i, opt in enumerate(q["options"], 1):
                print(f"{i}. {opt}")
            ans = input("Select option (1-4): ").strip()
            selected_option = q["options"][int(ans)-1] if ans.isdigit() and 1 <= int(ans) <= 4 else ""
            user_answers.append({
                "question": q["question"],
                "correct_answer": q["correct_answer"],
                "user_answer": selected_option
            })

        elif q["answer"].lower() in ["true", "false"]:  # True/False
            ans = input("Select (True/False): ").strip()
            user_answers.append({
                "question": q["question"],
                "correct_answer": q["answer"],
                "user_answer": ans
            })

        else:  # Fill in the Blank
            ans = input("Your Answer: ").strip()
            user_answers.append({
                "question": q["question"],
                "correct_answer": q["answer"],
                "user_answer": ans
            })

        print()

    evaluate_quiz(user_answers)


def evaluate_quiz(answers):
    """
    Sends user answers to the backend for evaluation and shows feedback.
    """
    response = requests.post(EVALUATE_API_URL, json={"answers": answers})

    if response.status_code != 200:
        print("❌ Error evaluating quiz:", response.json().get("error"))
        return

    result = response.json()
    print("\n🎯 Quiz Result:")
    print(f"Score: {result['score']} / {result['total']}")

    print("\n📝 Feedback:")
    for f in result["feedback"]:
        if f["correct"]:
            print(f"✅ {f['question']}")
        else:
            print(f"❌ {f['question']}")
            print(f"   Correct Answer: {f['correct_answer']}")

    # Save feedback to file
    generate_feedback_report(result["feedback"], result["score"], result["total"])


import os

FEEDBACK_FILE = "feedback_report.txt"  # Define a proper filename

def generate_feedback_report(feedback, score, total):
    """
    Saves feedback to a local file for download or printing.
    """
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        f.write(f"🎯 Score: {score} / {total}\n\n")
        f.write("📝 Feedback:\n")
        for entry in feedback:
            f.write(f"Q: {entry['question']}\n")
            if entry["correct"]:
                f.write("✅ Correct\n\n")
            else:
                f.write(f"❌ Incorrect\n")
                f.write(f"Correct Answer: {entry['correct_answer']}\n\n")

    print(f"\n📁 Feedback saved to: {FEEDBACK_FILE}")
    return os.path.abspath(FEEDBACK_FILE)  # <-- ✅ Return the absolute file path