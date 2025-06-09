import random
from transformers import pipeline
import re

# Initialize summarization pipeline to condense text into statements
try:
    summarizer # type: ignore
except NameError:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def modify_sentence(sentence):
    """Modify a sentence to introduce minor factual inaccuracies."""
    words = sentence.split()
    modified = False

    for i in range(len(words)):
        if re.match(r'\b\d+\b', words[i]):  # Look for numbers to change
            words[i] = str(int(words[i]) + random.choice([-1, 1]))  # Add/subtract 1
            modified = True
        elif words[i].lower() in ["is", "are", "was", "were", "has", "have"]:
            words[i] = random.choice(["isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't"])
            modified = True
        elif words[i].lower() in ["always", "never", "only"]:
            words[i] = random.choice(["sometimes", "often", "frequently", "rarely"])
            modified = True

    if not modified:
        random_word_index = random.randint(0, len(words) - 1)
        words[random_word_index] = "Not" + words[random_word_index]

    return " ".join(words)

def generate_true_false_questions(text, num_questions=5):
    """Generate true/false questions from text with more natural alterations."""
    # Truncate or split text to fit within the model's 1024 token limit
    text_chunks = []
    max_token_length = 1024
    while len(text) > max_token_length:
        # Find the last sentence boundary within the token limit
        last_period = text[:max_token_length].rfind(".")
        chunk = text[:last_period + 1]
        text_chunks.append(chunk.strip())
        text = text[last_period + 1:].strip()

    # Add the final chunk
    if text:
        text_chunks.append(text)

    # Summarize each chunk individually
    summaries = []
    for chunk in text_chunks:
        try:
            summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

    # Combine all summaries
    combined_summary = " ".join(summaries)
    sentences = combined_summary.split('. ')  # Split summary into sentences for questions

    # Generate True/False questions
    questions = []
    for sentence in sentences[:num_questions]:
        if random.choice([True, False]):
            # True statement
            questions.append((sentence.strip(), "True"))
        else:
            # Modify sentence for a False statement
            false_statement = modify_sentence(sentence.strip())
            questions.append((false_statement, "False"))

    return questions



# -----------------------Module testing code starts
# text = "Artificial intelligence is a field of computer science. It enables machines to learn and perform tasks."
# questions = generate_true_false_questions(text, num_questions=10)
# for question, answer in questions:
#     print("Question:", question, "| Answer:", answer)
# -----------------------Module testing code ends
# Status: Done Successful