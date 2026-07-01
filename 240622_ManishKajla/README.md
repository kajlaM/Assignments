# DocuMind AI Summer Project Assignments - Manish Kajla

This repository contains the complete deliverables for Assignment 1, Assignment 2, and Assignment 3 of the DocuMind AI Summer Project (July 2026).

---

## 🚀 Live Deployment (Assignment 3)
The FastAPI backend service is deployed and running live on Hugging Face Spaces:
👉 **[Hugging Face Space URL](https://huggingface.co/spaces/kajlamanish/documind_assignment_3_kajlamanish)**
👉 **[Interactive API Documentation (Swagger Docs)](https://kajlamanish-documind-assignment-3-kajlamanish.hf.space/docs)**

---

## 🔒 Security, Privacy & Confidentiality Audit
* **No Leaked Keys**: All API credentials (e.g., `GEMINI_API_KEY` and Hugging Face Access Tokens) are loaded dynamically via environment variables and system secrets. No production keys are hardcoded in the codebase.
* **Git Safety**: Local configuration files containing secret strings (such as `.env`), caches (`__pycache__/`), temporary folders, and vector database binaries (`data/`) are explicitly ignored by `.gitignore` and have **not** been committed.

---

## 📁 Repository Structure & Directory Index

### 📓 1. [Assignment_1.ipynb](Assignment_1.ipynb)
* **Goal**: Implement standard Python and NumPy computation fundamentals.
* **Topics Covered**:
  * **Temperature Analysis**: Standard list operations to filter temperatures and calculate averages.
  * **List Statistics**: Generating random integer lists and parsing maximum sum profiles.
  * **NumPy Arrays**: Performing high-speed array queries and computing standard deviations.
  * **OOP Book Management**: Simple Object-Oriented Programming (OOP) class containing title and author management helpers.

### 📓 2. [Assignment_2.ipynb](Assignment_2.ipynb)
* **Goal**: Build a complete local Retrieval-Augmented Generation (RAG) search pipeline.
* **Topics Covered**:
  * **Ingestion**: Reading files recursively and attaching standard metadata fields.
  * **Text Chunking**: Segmenting raw texts using `RecursiveCharacterTextSplitter`.
  * **Embeddings**: Creating local embedding vectors via HuggingFace's `SentenceTransformer("all-MiniLM-L6-v2")`.
  * **Vector DB**: Storing vectors inside persistent `ChromaDB` configured under the cosine distance space.
  * **Retrieval & Grounding**: Designing a custom `RAGRetriever` to extract top-k matches, score them via cosine similarity, and answer queries using a mock LLM generator.

### 📁 3. [Assignment_3/](Assignment_3/)
* **Goal**: Deploy a modular FastAPI web application container with advanced endpoints.
* **Completed Modules**:
  * **[Assignment_3/main.py](Assignment_3/main.py)**: Exposes API routes (`/`, `/chunk`, `/pdf`, `/csv`, `/ask`, `/generate-code`, `/generate-video`) with global exception handling and strict bounds checking.
  * **[Assignment_3/chunk.py](Assignment_3/chunk.py)**: Logical text segmenter module using Recursive Character splitters.
  * **[Assignment_3/pdf_utils.py](Assignment_3/pdf_utils.py)**: Extracts text content and counts pages from PDF files using `pypdf`.
  * **[Assignment_3/csv_utils.py](Assignment_3/csv_utils.py)**: Formats tabular CSV structures into plain text tables using `pandas`.
  * **[Assignment_3/llm_utils.py](Assignment_3/llm_utils.py)**: Integrates with the new `google-genai` SDK and extracts Python source code blocks out of Markdown strings.
  * **[Assignment_3/manim_pipeline.py](Assignment_3/manim_pipeline.py)**: Automatically generates and compiles Manim animations from prompts. Enforces strict text rules (banning `Tex()` and `MathTex()` to compile without LaTeX system requirements) and self-heals by recycling compilation logs back into the LLM up to 3 times on syntax errors.
  * **[Assignment_3/Dockerfile](Assignment_3/Dockerfile)**: Docker instructions installing system dependencies (FFmpeg, Pango, Cairo libraries) and booting the app securely on Hugging Face Spaces.
  * **[Assignment_3/README.md](Assignment_3/README.md)**: Standard configuration documentation for local running and testing.
