import os
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import modular helper dependencies
from chunk import chunk_text
# Note: Stubs or files for these imports will be written in the next steps
from pdf_utils import extract_text_from_pdf
from csv_utils import extract_text_from_csv
from llm_utils import GeminiClient
from manim_pipeline import render_manim_video

# Initialize FastAPI app
app = FastAPI(
    title="DocuMind AI Backend",
    description="FastAPI Service for Document Parsing, Chunking, and AI-to-Manim Animation Rendering",
    version="1.0.0"
)

# Enable CORS for frontend and space compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure application directories exist
UPLOAD_DIR = Path("uploads")
GENERATED_DIR = Path("generated")
TEMP_DIR = Path("temp")

for directory in [UPLOAD_DIR, GENERATED_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Pydantic schemas for request validation
class ChunkRequest(BaseModel):
    text: str = Field(..., description="The large text content to chunk.")

class AskRequest(BaseModel):
    query: str = Field(..., description="The query to send to the Gemini model.")

class CodeGenRequest(BaseModel):
    prompt: str = Field(..., description="Prompt instructing the AI to write Python code.")

class VideoGenRequest(BaseModel):
    idea: str = Field(..., description="The scene animation idea to render via Manim.")

# Initialize Gemini Client
gemini_client = GeminiClient()


# =====================================================================
# Endpoint 1: Welcome Greeting
# =====================================================================
@app.get("/", summary="Welcome greeting endpoint")
async def welcome() -> Dict[str, str]:
    return {"message": "Welcome to DocuMind Assignment 3"}


# =====================================================================
# Endpoint 2: Text Chunking
# =====================================================================
@app.post("/chunk", summary="Splits raw text into overlapping chunks")
async def chunk_endpoint(
    request: ChunkRequest,
    chunk_size: int = Query(50, description="Max chunk size (characters)"),
    chunk_overlap: int = Query(10, description="Overlap size between chunks")
) -> Dict[str, Any]:
    # 1. Validation checks
    text = request.text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty."
        )
    if chunk_size <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chunk size must be a positive integer."
        )
    if chunk_overlap < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chunk overlap cannot be negative."
        )
    if chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chunk overlap must be strictly less than chunk size."
        )

    # 2. Run chunking helper
    try:
        chunks = chunk_text(text, chunk_size, chunk_overlap)
        return {
            "chunks": chunks,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during text chunking: {str(e)}"
        )


# =====================================================================
# Endpoint 3 (Feature 1): PDF Upload & Extraction
# =====================================================================
@app.post("/pdf", summary="Upload a PDF file and extract text content")
async def upload_pdf(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files (.pdf) are supported."
        )

    file_path = UPLOAD_DIR / file.filename
    try:
        # Save upload file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Run parser
        parsed_data = extract_text_from_pdf(str(file_path))
        return {
            "filename": file.filename,
            "pages": parsed_data["pages"],
            "text": parsed_data["text"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing PDF file: {str(e)}"
        )
    finally:
        # Clean up temporary uploaded file
        if file_path.exists():
            os.remove(file_path)


# =====================================================================
# Endpoint 4 (Feature 2): CSV Upload & Conversion
# =====================================================================
@app.post("/csv", summary="Upload a CSV file and convert to plain text format")
async def upload_csv(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files (.csv) are supported."
        )

    file_path = UPLOAD_DIR / file.filename
    try:
        # Save upload file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Run parser
        plain_text = extract_text_from_csv(str(file_path))
        return {
            "filename": file.filename,
            "text": plain_text
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing CSV file: {str(e)}"
        )
    finally:
        # Clean up temporary uploaded file
        if file_path.exists():
            os.remove(file_path)


# =====================================================================
# Endpoint 5 (Feature 3): LLM Question/Answering
# =====================================================================
@app.post("/ask", summary="Ask a question to the Gemini LLM model")
async def ask_llm(request: AskRequest) -> Dict[str, str]:
    query = request.query.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty."
        )

    try:
        answer = gemini_client.ask_gemini(query)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM generation failed: {str(e)}"
        )


# =====================================================================
# Endpoint 6 (Feature 4): AI Python Code Generator
# =====================================================================
@app.post("/generate-code", summary="Generates and parses clean Python code from prompts")
async def generate_code(request: CodeGenRequest) -> Dict[str, str]:
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt cannot be empty."
        )

    try:
        clean_code = gemini_client.generate_code(prompt)
        return {"code": clean_code}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {str(e)}"
        )


# =====================================================================
# Endpoint 7 (Feature 5): AI-to-Manim Rendering Pipeline
# =====================================================================
@app.post("/generate-video", summary="Generates Manim animation videos from prompt ideas")
async def generate_video(request: VideoGenRequest) -> Dict[str, Any]:
    idea = request.idea.strip()
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Animation idea cannot be empty."
        )

    try:
        video_path = render_manim_video(idea)
        return {
            "status": "success",
            "idea": idea,
            "video_path": video_path
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video rendering pipeline failed: {str(e)}"
        )
