import pandas as pd

def extract_text_from_csv(file_path: str) -> str:
    """
    Reads a CSV file and converts it into a formatted plain-text string representation.
    
    Args:
        file_path (str): The local path to the CSV file.
        
    Returns:
        str: A clean, formatted plain-text table layout of the CSV.
    """
    try:
        # Load the CSV file using pandas
        df = pd.read_csv(file_path)
        # Convert the DataFrame to a plain-text grid without row index numbers
        return df.to_string(index=False)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {str(e)}")
