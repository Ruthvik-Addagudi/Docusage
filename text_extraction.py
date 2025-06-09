import fitz  # type: ignore # PyMuPDF for PDF extraction
import os

# Supported file formats
SUPPORTED_FORMATS = {".pdf", ".txt", ".docx"}

def extract_text_with_PyMuPDF(file_path):
    """Determines file type and extracts text using the appropriate function."""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in SUPPORTED_FORMATS:
        return f"Error: Unsupported file type. Supported formats: {', '.join(SUPPORTED_FORMATS)}"

    try:
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension == ".txt":
            return extract_text_from_txt(file_path)
        elif file_extension == ".docx":
            return extract_text_from_docx(file_path)
    except FileNotFoundError:
        return "Error: The file was not found. Please check the file path."
    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF document using PyMuPDF."""
    with fitz.open(file_path) as pdf:
        return "\n".join(page.get_text() for page in pdf)

def extract_text_from_txt(file_path):
    """Extracts text from a plain text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text_from_docx(file_path):
    """Extracts text from a Word document (.docx)."""
    try:
        from docx import Document  # Import only if needed
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except ImportError:
        return "Error: Missing 'python-docx' library. Install it using 'pip install python-docx'."

# ---------------------------Module testing code starts
if __name__ == "__main__":
    # Test with different file types
    test_files = [
        "C:\\Users\\Sathvik\\Desktop\\DocuSage\\Projectcode\\sample.pdf",
        "C:\\Users\\Sathvik\\Desktop\\DocuSage\\Projectcode\\sample.txt",
        "C:\\Users\\Sathvik\\Desktop\\DocuSage\\Projectcode\\sample.docx",
        "C:\\Users\\Sathvik\\Desktop\\DocuSage\\Projectcode\\unsupported.xyz"
    ]

    for file in test_files:
        print(f"\nProcessing: {file}")
        print(extract_text_with_PyMuPDF(file))
# ---------------------------Module testing code ends