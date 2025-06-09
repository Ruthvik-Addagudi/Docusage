import string
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")
FILLER_WORDS = set(spacy.lang.en.stop_words.STOP_WORDS)

def split_text(text, max_length=1000):
    """Splits text into smaller chunks for summarization."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 for space
        if current_length > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = len(word) + 1
        current_chunk.append(word)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def filter_keywords(words):
    """Filters out filler words and punctuation, returning a cleaned list of keywords."""
    cleaned_words = [
        word.lower() for word in words
        if word.lower() not in FILLER_WORDS and word not in string.punctuation and len(word) > 2
    ]
    return cleaned_words

#------------------------Module testing code starts
if __name__ == "__main__":
    # Sample text for testing
    sample_text = """Machine learning and artificial intelligence are rapidly evolving fields.
    This module will split the text and filter keywords for cleaner input."""

    # Test split_text function
    # chunks = split_text(sample_text, max_length=20)
    # print("Text chunks after splitting:\n", chunks)

    # Test filter_keywords function
#    sample_words = sample_text.split()
#    filtered_keywords = filter_keywords(sample_words)
#    print("Filtered keywords:\n", filtered_keywords)
#-----------------------Module testing code ends
#Status: Done succesfully