# AI Summer Project Assignments - Manish Kajla

This directory contains the completed and executed Jupyter Notebook assignments for the AI Summer Project.

## Deliverables

### 1. `Assignment_1.ipynb` (Python & NumPy Basics)
* **Goal**: Implement standard Python data-analysis procedures and NumPy operations.
* **Topics Covered**:
  * Filtering temperatures strictly greater than a threshold and calculating their average (`analyze_temperatures`).
  * Generating multiple lists of random integers and tracking maximum sum statistical profiles.
  * Performing fast array indexing and computing standard deviations using NumPy functions.
  * Creating a library management `Book` class showcasing Object-Oriented Programming (OOP) properties.

### 2. `Assignment_2.ipynb` (RAG Pipeline)
* **Goal**: Build a complete, functional Retrieval-Augmented Generation (RAG) pipeline from scratch.
* **Topics Covered**:
  * **Part 1: Data Ingestion**: Recursive PDF document loading from directories, appending standard metadata fields (`source_file` and `file_type`).
  * **Part 2: Chunking**: Splitting files into logical parts using `RecursiveCharacterTextSplitter` configured for appropriate chunk sizes (1000) and overlap factors (200).
  * **Part 3: Embedding**: Wrapping HuggingFace's `SentenceTransformer("all-MiniLM-L6-v2")` to generate local vector embeddings.
  * **Part 4: Vector DB**: persisting data in local `ChromaDB` configured under the cosine distance metrics space.
  * **Part 5 & 6: Retrieval & Similarity Search**: Custom retrieval class extracting top-k matches and converting scores correctly.
  * **Part 7 & 8: Simple & Advanced RAG**: Pipeline implementation linking retrieval matches to a Mock LLM wrapper simulating streaming prompts, citation indexing, and chat history storage.

---

## How to Run locally

### 1. Install dependencies
Install the required packages in your Python environment:
```bash
pip install sentence-transformers chromadb langchain langchain-community scikit-learn pypdf
```

### 2. Open the notebooks
Launch Jupyter Notebook or JupyterLab:
```bash
jupyter notebook
```
Open `Assignment_1.ipynb` or `Assignment_2.ipynb` and run the cells from top to bottom.
