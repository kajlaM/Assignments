from typing import Dict, Any
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extracts text and counts the total pages of a given PDF file.
    
    Args:
        file_path (str): The local path to the PDF file.
        
    Returns:
        Dict[str, Any]: A dictionary containing 'pages' count and 'text' content.
    """
    try:
        reader = PdfReader(file_path)
        pages_count = len(reader.pages)
        text_content = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
                
        return {
            "pages": pages_count,
            "text": "\n".join(text_content)
        }
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")
