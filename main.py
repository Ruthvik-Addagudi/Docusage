from text_extraction import extract_text_with_PyMuPDF
from summarization import summarize_text
from concept_extraction import extract_key_concepts, prioritize_side_headings
from mind_map_generation import create_mind_map
from true_false_generator import generate_true_false_questions
from mcq_generator import generate_all_questions
from fill_in_the_blanks_generator import generate_fill_in_the_blanks
from evaluation import evaluate_true_false, evaluate_fill_in_the_blanks, evaluate_mcq, provide_feedback

def generate_summarized_mind_map_and_questions(file_path):
    """Main function to extract, summarize, generate a mind map, generate questions, and evaluate them."""
    
    # Step 1: Extract Text
    print("Extracting text from PDF...")
    text = extract_text_with_PyMuPDF(file_path)
    assert text, "Error: Text extraction failed - No text found in PDF."
    print("Text extraction successful.\n")
    
    # Step 2: Summarize Text
    print("Summarizing the extracted text...")
    summarized_text = summarize_text(text)
    assert summarized_text, "Error: Summarization failed - No summary generated."
    print("Summary of PDF:\n", summarized_text)
    
    # Step 3: Extract Key Concepts
    print("\nExtracting key concepts from the summary...")
    key_concepts = extract_key_concepts(summarized_text)
    assert key_concepts, "Error: Key concept extraction failed - No concepts extracted."
    print("Key concepts extracted:", key_concepts)
    
    # Step 4: Prioritize Side Headings
    print("\nPrioritizing side headings in the key concepts...")
    prioritized_concepts = prioritize_side_headings(summarized_text, key_concepts)
    assert prioritized_concepts, "Error: Side headings prioritization failed - No prioritized concepts."
    print("Prioritized concepts:", prioritized_concepts)
    
    # Step 5: Generate Mind Map
    print("\nGenerating the mind map...")
    create_mind_map(prioritized_concepts)
    print("Mind map generation successful.\n")
    
    # Step 6: Generate Questions
    print("Generating True/False questions...")
    true_false_questions = generate_true_false_questions(summarized_text, num_questions=3)
    print("True/False Questions Generated:", true_false_questions)
    
    print("\nGenerating MCQ questions...")
    mcq_questions = generate_all_questions(summarized_text)
    print("MCQ Questions Generated:", mcq_questions)
    
    print("\nGenerating Fill-in-the-Blank questions...")
    fill_in_the_blank_questions = generate_fill_in_the_blanks(summarized_text)
    print("Fill-in-the-Blank Questions Generated:", fill_in_the_blank_questions)
    
    # Store the result for further verification if needed
    return {
        "text": text,
        "summary": summarized_text,
        "key_concepts": key_concepts,
        "prioritized_concepts": prioritized_concepts,
        "true_false_questions": true_false_questions,
        "mcq_questions": mcq_questions,
        "fill_in_the_blank_questions": fill_in_the_blank_questions
    }

#--------------------------Integration Testing Code Starts
if __name__ == "__main__":
    file_path = "C:\\Users\\Sathvik\\Desktop\\DocuSage\\Projectcode\\computer basics.pdf"  # Replace with your actual file path
    
    try:
        results = generate_summarized_mind_map_and_questions(file_path)
        print("\nIntegration testing completed successfully.\nResults:", results)
    except AssertionError as e:
        print("Integration testing failed:", e)
#-------------------------Integration Testing Code Ends
