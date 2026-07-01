---
title: Documind Assignment 3 Kajlamanish
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Summer Project Assignments - Manish Kajla

This directory contains the completed assignments for the AI Summer Project.

---

## Workspace Layout

```
240622_ManishKajla/
│
├── Assignment_1.ipynb          # Python & NumPy Basics (Submitted & Untouched)
├── Assignment_2.ipynb          # Retrieval-Augmented Generation (Submitted & Untouched)
│
├── main.py                     # FastAPI Entry point (App routes and input validations)
├── chunk.py                    # RecursiveCharacterTextSplitter chunking logic
├── pdf_utils.py                # PDF text and page extraction logic
├── csv_utils.py                # CSV to plain-text converter
├── llm_utils.py                # Gemini model interface and markdown python code parsing
├── manim_pipeline.py           # Self-healing Manim animation generator
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container instructions
├── .env.example                # Environment template
└── README.md                   # Project documentation
```

---

## 1. Notebooks (Assignment 1 & 2)

* **Assignment_1.ipynb**: Contains implementations of standard Python data operations, random list statistics, NumPy array selections, and an OOP `Book` class.
* **Assignment_2.ipynb**: Contains a complete local RAG search indexing and retrieval pipeline. Uses the `all-MiniLM-L6-v2` transformer model for local embeddings, persistent ChromaDB for storage, and a custom retrieval interface with mock LLM grounding, streaming outputs, and query logs.

---

## 2. FastAPI Backend (Assignment 3)

The backend exposes a highly robust REST API to chunk large texts, upload & parse files, perform LLM generation, and compile dynamic animations using the Manim pipeline.

### Prerequisites (For Local Execution)
To render Manim video animations on your local system, you must install the `ffmpeg` binary:
* **macOS** (via Homebrew):
  ```bash
  brew install ffmpeg
  ```
* **Ubuntu/Debian**:
  ```bash
  sudo apt-get update && sudo apt-get install -y ffmpeg
  ```

### Local Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment keys in a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
4. Run the development server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. View API docs: Navigate to `http://localhost:8000/docs`.

### API Endpoints

* **GET /** Welcome greeting.
* **POST /chunk?chunk_size=50&chunk_overlap=10**
  Splits request body text into Recursive Character chunks. Validates size/overlap parameters.
* **POST /pdf** (Multipart Form Upload)
  Extracts text content and returns filename, page counts, and text representation.
* **POST /csv** (Multipart Form Upload)
  Converts tabular CSV rows into a plain-text grid format.
* **POST /ask**
  Submits questions to the Google Gemini model.
* **POST /generate-code**
  Requests Python code from a prompt and parses clean code out of Markdown fences.
* **POST /generate-video**
  Spawns the AI-to-Manim rendering pipeline. Uses Gemini to draft script scenes, compile them, self-heal upon syntax errors up to 3 retries, and returns the rendered `.mp4` video.

---

## Deployment Instructions

### 1. Render Deployment
1. Go to your [Render Dashboard](https://dashboard.render.com/) and create a **Web Service**.
2. Connect your GitHub repository.
3. Select **Docker** as the Environment.
4. Under Environment variables, configure:
   * `GEMINI_API_KEY`: `your_actual_api_key`
5. Click deploy. Render will build the container using the provided `Dockerfile` and expose it.

### 2. Hugging Face Spaces Deployment
1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space).
2. Set Space SDK to **Docker**, and choose the **Blank** template.
3. Commit this workspace folder (`240622_ManishKajla/`) along with your files.
4. Add your API key in Space Settings under **Repository Secrets** as:
   * Name: `GEMINI_API_KEY`
   * Value: `your_actual_api_key`
5. Hugging Face will build the container and deploy the app at port `7860` automatically.
