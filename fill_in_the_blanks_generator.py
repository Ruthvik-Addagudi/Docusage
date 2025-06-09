import spacy # type: ignore
import random

# Load spaCy's language model
try:
    nlp # type: ignore
except NameError:
    nlp = spacy.load("en_core_web_sm")

def generate_fill_in_the_blanks(text, num_questions=3):
    """Generate fill-in-the-blank questions from text."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    questions = []
    for sentence in sentences[:num_questions]:
        doc_sent = nlp(sentence)
        # Find a noun or proper noun to blank out
        blanks = [token.text for token in doc_sent if token.pos_ in ["NOUN", "PROPN"]]
        if blanks:
            blank_word = random.choice(blanks)
            question = sentence.replace(blank_word, "_____")
            questions.append((question, blank_word))
    
    return questions


#------------------------Module testing code starts
# text = "Artificial intelligence is a field of computer science. It enables machines to learn and perform tasks."
# questions = generate_fill_in_the_blanks(text)
# for question, answer in questions:
#     print("Question:", question, "| Answer:", answer)
#------------------------Module testing code ends
#Status: Done successful
