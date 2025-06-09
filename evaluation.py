# evaluation.py

def evaluate_true_false(user_answer, correct_answer):
    """Evaluate a true/false question."""
    return user_answer.lower() == correct_answer.lower()

def evaluate_fill_in_the_blanks(user_answer, correct_answer):
    """Evaluate a fill-in-the-blank question."""
    return user_answer.strip().lower() == correct_answer.lower()

def evaluate_mcq(user_answer, correct_answer):
    """Evaluate an MCQ question."""
    return user_answer.strip().lower() == correct_answer.lower()

def provide_feedback(correct, question_type):
    """Provide feedback based on the evaluation result."""
    if correct:
        return f"Correct! Great job on the {question_type} question."
    else:
        return f"Incorrect. Keep practicing the {question_type} question for improvement."

#-----------------------------Module testing code starts(more code is in test_evaluation.py which is in test folder)
result = evaluate_true_false("True", "True")
print(provide_feedback(result, "True/False"))
#-----------------------------Module testing code ends
#Status: Done successful
