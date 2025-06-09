from transformers import pipeline
from modules.text_preprocessing import split_text  # Import split_text function

# Initialize summarization pipeline with a specified model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_long_text(text, summarizer, max_length=200, min_length=50):
    """Summarizes long text by dividing it into manageable chunks."""
    summary = ""
    chunks = split_text(text)

    # if chunks:
    #     print("First chunk to be summarized:\n", chunks[0], "\n")

    for chunk in chunks:
        summary_chunk = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summary += summary_chunk[0]['summary_text'] + " "
    return summary.strip()


def summarize_text(text, max_length=200, min_length=50):
    return summarize_long_text(text, summarizer, max_length, min_length)


#------------------------------Module testing code starts
if __name__ == "__main__":
    # Sample text for testing
    sample_text = """Machine learning enables computers to learn from data without being explicitly programmed. 
    It is widely used in a range of applications like recommendation systems, image recognition, and more."""

    # Test summarize_text function
    summary = summarize_text(sample_text, max_length=30, min_length=20)
    print("Summary of the sample text:\n", summary)
#------------------------------Module testing code ends
#Status: Done Successful