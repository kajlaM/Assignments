---
title: Documind Assignment 3 Kajlamanish
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# DocuMind Assignment 3 - FastAPI Backend Application

A modular, production-ready FastAPI application that implements standard text chunking, PDF/CSV parsing, Gemini LLM queries, and an automated AI-to-Manim video rendering pipeline.

---

## 🚀 Live Deployment Links
The backend is deployed and running live on Hugging Face Spaces. Below are the two different URLs:

1. **Hugging Face Space Dashboard (For Submission)**:
   👉 **[Hugging Face Space URL](https://huggingface.co/spaces/kajlamanish/documind_assignment_3_kajlamanish)**
   *Use this link for project submissions. It hosts the build status, repository files, settings, and logs.*

2. **Direct API Swagger Documentation (For Testing)**:
   👉 **[Interactive API Documentation (Swagger Docs)](https://kajlamanish-documind-assignment-3-kajlamanish.hf.space/docs)**
   *Use this link to run and test all the FastAPI endpoints (`/chunk`, `/pdf`, `/csv`, `/ask`, `/generate-code`, `/generate-video`) directly in your browser.*

---

## Folder Structure

```
documind/
├── main.py                     # Entry point (App routes and input validations)
├── chunk.py                    # RecursiveCharacterTextSplitter chunking logic
├── pdf_utils.py                # PDF text and page extraction logic
├── csv_utils.py                # CSV to plain-text converter
├── llm_utils.py                # Gemini model interface and markdown python code parsing
├── manim_pipeline.py           # Self-healing Manim animation generator
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container instructions
├── README.md                   # Setup instructions
├── uploads/                    # Scratch folder for uploaded files
├── generated/                  # Destination directory for rendered .mp4 files
└── temp/                       # Working directory for compiler scenes
```

---

## Installation & Local Setup

### 1. Prerequisites
To run the Manim video generator locally, you must install the `ffmpeg` system binary:
* **macOS** (using Homebrew):
  ```bash
  brew install ffmpeg
  ```
* **Ubuntu/Debian**:
  ```bash
  sudo apt-get update && sudo apt-get install -y ffmpeg
  ```
* **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/) and add it to your system PATH.

### 2. Configure Virtual Environment
Set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the root directory (based on `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Running the App Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

---

## API Endpoints

### 1. Welcome Greeting
* **GET** `/`
* **Response**:
  ```json
  {"message": "Welcome to DocuMind Assignment 3"}
  ```

### 2. Text Chunking
* **POST** `/chunk?chunk_size=50&chunk_overlap=10`
* **Payload**:
  ```json
  {"text": "Your large text to chunk goes here."}
  ```
* **Response**:
  ```json
  {
    "chunks": ["Your large text to", "text to chunk goes here."],
    "total_chunks": 2
  }
  ```

### 3. PDF Upload
* **POST** `/pdf` (Multipart form-data: upload a `.pdf` file)
* **Response**:
  ```json
  {
    "filename": "document.pdf",
    "pages": 5,
    "text": "Extracted text content from pages..."
  }
  ```

### 4. CSV Upload
* **POST** `/csv` (Multipart form-data: upload a `.csv` file)
* **Response**:
  ```json
  {
    "filename": "table.csv",
    "text": "Plain text table grid representation of rows..."
  }
  ```

### 5. Ask Gemini LLM
* **POST** `/ask`
* **Payload**:
  ```json
  {"query": "Explain quantum physics in one sentence."}
  ```
* **Response**:
  ```json
  {"response": "Quantum physics describes the behavior of matter and energy on microscopic scales..."}
  ```

### 6. Generate Python Code
* **POST** `/generate-code`
* **Payload**:
  ```json
  {"prompt": "Write a python function to check if a number is prime."}
  ```
* **Response**:
  ```json
  {
    "code": "def is_prime(n):\n    if n <= 1:\n        return False\n..."
  }
  ```

### 7. AI-to-Manim Rendering
* **POST** `/generate-video`
* **Payload**:
  ```json
  {"idea": "Draw a blue circle that expands and turns into a yellow square."}
  ```
* **Response**:
  ```json
  {
    "status": "success",
    "idea": "Draw a blue circle that expands and turns into a yellow square.",
    "video_path": "generated/render_20260702_010000_ExpandCircle.mp4"
  }
  ```

---

## Deployment

### Option 1: Render
1. Create a Web Service on [Render](https://dashboard.render.com/).
2. Connect your GitHub repository.
3. Select **Docker** as the Environment.
4. Under Environment variables, configure:
   * `GEMINI_API_KEY`: `your_actual_key`
5. Click deploy. Render will build the container using the provided `Dockerfile` and expose port `7860`.

### Option 2: Hugging Face Spaces
1. Go to [Hugging Face Spaces](https://huggingface.co/new-space).
2. Choose Space SDK: **Docker**.
3. Select Docker Template: **Blank**.
4. In your repository files, commit the `Dockerfile`, `requirements.txt`, and your application code.
5. In Space Settings, add your API key in **Repository Secrets** as:
   * Name: `GEMINI_API_KEY`
   * Value: `your_actual_key`
6. Hugging Face will build the Docker container and host the app at port `7860` automatically.
