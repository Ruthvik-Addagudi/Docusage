from collections import Counter
import spacy
from .text_preprocessing import filter_keywords  # Import filter_keywords from text_preprocessing.py

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

def extract_key_concepts(text, max_words=25):
    """Extracts key concepts (frequent nouns, noun chunks, and named entities) from the text."""
    doc = nlp(text)
    word_freq = Counter()

    # Extracting noun chunks and named entities
    for chunk in doc.noun_chunks:
        word_freq.update(filter_keywords(chunk.text.split()))

    for ent in doc.ents:
        word_freq.update(filter_keywords(ent.text.split()))

    # Get the most common words
    most_common_words = [word for word, freq in word_freq.most_common(max_words)]
    
    return most_common_words

def prioritize_side_headings(text, concepts):
    """Prioritizes side headings from the PDF as high-priority keywords in the mind map."""
    doc = nlp(text)
    side_headings = [sent.text.strip() for sent in doc.sents if sent.text.strip().isupper()]
    
    for heading in side_headings:
        if heading.lower() in concepts:
            concepts.remove(heading.lower())
            concepts.insert(0, heading.lower())  # Add at the beginning
    return concepts

#--------------------------Module testing code starts
if __name__ == "__main__":
    # Sample text for testing
    sample_text = """MACHINE LEARNING OVERVIEW
    Machine learning involves algorithms that allow computers to learn patterns from data. 
    Applications include healthcare, finance, and more."""

    # Test extract_key_concepts function
    key_concepts = extract_key_concepts(sample_text, max_words=10)
    print("Extracted key concepts:\n", key_concepts)

    # Test prioritize_side_headings function
    prioritized_concepts = prioritize_side_headings(sample_text, key_concepts)
    print("Prioritized concepts with side headings:\n", prioritized_concepts)

#--------------------------Module testing code ends
#Status: Done Successful