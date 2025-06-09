import random
import re
from transformers import pipeline
import spacy # type: ignore

def get_summarizer():
    """Lazy initialization for the summarizer model."""
    return pipeline("summarization", model="facebook/bart-large-cnn")

def get_nlp():
    """Lazy initialization for the SpaCy NLP model."""
    return spacy.load("en_core_web_sm")

def summarize_text(text, max_length=150, min_length=50):
    summarizer = get_summarizer()
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text  # Fallback to the original text if summarization fails

def extract_keywords(text, max_keywords=5):
    nlp = get_nlp()
    doc = nlp(text)
    keywords = [chunk.text.strip() for chunk in doc.noun_chunks][:max_keywords]
    return keywords


def generate_mcq(sentence, num_options=4):
    """
    Generate a single multiple-choice question (MCQ) from a sentence.
    """
    keywords = extract_keywords(sentence)
    if len(keywords) < 2:
        return None  # Not enough keywords to generate a meaningful question

    # Construct the question and correct answer
    question = f"What is the significance of '{keywords[0]}' in the context of the text?"
    correct_answer = keywords[0]

    # Generate distractors from remaining keywords
    distractors = keywords[1:num_options]
    while len(distractors) < num_options - 1:
        distractors.append(f"Random option {len(distractors) + 1}")  # Add filler options if needed

    # Shuffle options
    options = [correct_answer] + distractors
    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }


def generate_mcqs(text, num_questions=3):
    """
    Generate multiple MCQs from the provided text.
    """
    summarized_text = summarize_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', summarized_text)

    mcqs = []
    for sentence in sentences:
        if len(mcqs) >= num_questions:
            break
        mcq = generate_mcq(sentence)
        if mcq:
            mcqs.append(mcq)

    # Add placeholders if there aren't enough questions
    while len(mcqs) < num_questions:
        mcqs.append({
            "question": "Placeholder question due to insufficient data.",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A"
        })

    return mcqs


# -----------------------Module testing code starts
if __name__ == "__main__":
    text = (
        "Machine learning is a subset of artificial intelligence. "
        "It allows machines to learn from data and make decisions. "
        "Key concepts include algorithms, neural networks, and large datasets."
    )

    mcqs = generate_mcqs(text, num_questions=3)

    for i, mcq in enumerate(mcqs, 1):
        print(f"MCQ {i}: {mcq['question']}")
        print(f"Options: {mcq['options']}")
        print(f"Correct Answer: {mcq['correct_answer']}\n")
# -----------------------Module testing code ends
