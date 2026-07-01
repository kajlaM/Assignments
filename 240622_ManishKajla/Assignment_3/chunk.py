from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 50, chunk_overlap: int = 10) -> List[str]:
    """
    Splits a large input text into smaller segments using RecursiveCharacterTextSplitter.
    
    Args:
        text (str): The raw input text.
        chunk_size (int): Max character count per chunk.
        chunk_overlap (int): Overlap size between consecutive chunks.
        
    Returns:
        List[str]: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    # split_text splits a single string document
    return text_splitter.split_text(text)
