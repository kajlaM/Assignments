import os
import re
import sys
import datetime
import subprocess
import glob
import shutil
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Set up directory paths
TEMP_DIR = Path("temp")
GENERATED_DIR = Path("generated")

def ask_ai_for_manim_code(prompt: str, error_feedback: str = None, previous_code: str = None) -> str:
    """
    Asks Gemini to generate valid Manim scene Python code.
    If error_feedback is provided, asks the AI to self-heal/correct the previous code.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not configured.")
    client = genai.Client(api_key=api_key)

    system_prompt = (
        "You are an expert Python developer and an expert in the Manim Community Edition animation library.\n"
        "Your output must consist ONLY of valid, executable Python code inside standard code blocks.\n"
        "Do NOT include any explanations, warnings, greetings, or markdown outside of standard python code blocks.\n\n"
        "Strict Manim Generation Rules:\n"
        "1. Always begin your code with:\n"
        "from manim import *\n\n"
        "2. Never use Tex() or MathTex(). These require LaTeX compilers which are not available.\n"
        "3. Only use Text() for all text, math equations, and labels.\n"
        "4. Always animate elements using self.play(). Never rely on self.add() to just display them without animation.\n"
        "5. Use self.wait() between logical animation steps to give the viewer time to follow.\n"
        "6. If the user requests a 3D animation:\n"
        "   - The scene class must inherit from ThreeDScene.\n"
        "   - You must call self.set_camera_orientation(...) in the construct method.\n"
        "7. Space objects properly using shift(), next_to(), or move_to() to avoid overlapping.\n"
        "8. Rate functions must always use 'rate_functions.smooth' instead of 'smooth'.\n"
        "9. Make sure the scene class inherits from Scene (or ThreeDScene) and implements a construct(self) method.\n"
        "10. Return ONLY Python code. No text before or after the code block."
    )

    if error_feedback and previous_code:
        user_content = (
            f"The previous Manim Python code generated for the prompt \"{prompt}\" failed to compile or render.\n"
            f"Here is the generated code that failed:\n"
            f"```python\n"
            f"{previous_code}\n"
            f"```\n\n"
            f"Here is the error message / stack trace from the rendering process:\n"
            f"{error_feedback}\n\n"
            f"Please fix the error(s). Preserve the original concept but ensure the syntax and Manim function calls are correct "
            f"and compile successfully. Make sure to NEVER use Tex() or MathTex() - use ONLY Text(). "
            f"Return ONLY the corrected Python code inside a python code block."
        )
    else:
        user_content = f"Generate a Manim scene for the following prompt: {prompt}"

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API request failed during Manim code generation: {str(e)}")

def extract_python_code(raw_text: str) -> str:
    """Extracts python code from raw text markdown backticks"""
    if not raw_text:
        return ""
    
    # Match markdown block ```python ... ``` or ``` ... ```
    pattern = r"```(?:python)?\s*(.*?)\s*```"
    match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
        
    return raw_text.strip()

def get_scene_class_name(code: str) -> str:
    """Extracts the Scene class name from the generated python code"""
    pattern = r"class\s+(\w+)\s*\((?:Scene|ThreeDScene|VectorScene|LinearTransformationScene|MovingCameraScene|MovingCamera|GraphScene)\)"
    match = re.search(pattern, code)
    if match:
        return match.group(1)
        
    pattern_fallback = r"class\s+(\w+)\s*\("
    match_fallback = re.search(pattern_fallback, code)
    if match_fallback:
        return match_fallback.group(1)
        
    return None

def render_manim_video(idea: str) -> str:
    """
    Generates Manim code for an idea, compiles it, self-heals up to 3 times on compilation error,
    and returns the saved path of the output MP4 video.
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    max_retries = 3
    current_retry = 0
    error_feedback = None
    previous_code = None

    # Determine binary paths
    manim_bin = shutil.which("manim")

    while current_retry <= max_retries:
        print(f"Generating Manim code for idea: '{idea}' (Attempt {current_retry + 1}/{max_retries + 1})...")
        
        # 1. Generate Manim code
        raw_response = ask_ai_for_manim_code(idea, error_feedback, previous_code)
        code = extract_python_code(raw_response)
        previous_code = code

        # 2. Save script file to temp directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        script_name = f"scene_{timestamp}_try{current_retry}"
        script_file_path = TEMP_DIR / f"{script_name}.py"

        with open(script_file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 3. Extract the class name
        scene_name = get_scene_class_name(code)
        if not scene_name:
            error_feedback = "No class definition inheriting from Scene or ThreeDScene found in code."
            current_retry += 1
            print(f"Healing triggered: {error_feedback}")
            continue

        # 4. Render command construction
        # Output to subfolder in generated/ via --media_dir
        if manim_bin:
            cmd = [manim_bin, "-ql", "-v", "WARNING", "--media_dir", str(GENERATED_DIR), str(script_file_path), scene_name]
        else:
            cmd = [sys.executable, "-m", "manim", "-ql", "-v", "WARNING", "--media_dir", str(GENERATED_DIR), str(script_file_path), scene_name]

        print(f"Running Manim CLI: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=120  # Avoid freezing
            )
            
            if result.returncode == 0:
                # Compile succeeded! Search for generated video
                # Manim media structure: generated/videos/<script_name>/480p15/<scene_name>.mp4
                search_pattern = str(GENERATED_DIR / "videos" / script_name / "**" / "*.mp4")
                mp4_files = glob.glob(search_pattern, recursive=True)
                
                if mp4_files:
                    src_file = mp4_files[0]
                    # Copy to a flat destination path in generated directory
                    dest_file_name = f"render_{timestamp}_{scene_name}.mp4"
                    dest_file_path = GENERATED_DIR / dest_file_name
                    shutil.copy2(src_file, dest_file_path)
                    
                    # Clean up temporary videos subfolders
                    try:
                        shutil.rmtree(GENERATED_DIR / "videos")
                    except Exception:
                        pass
                        
                    print(f"Video successfully rendered at: {dest_file_path}")
                    return str(dest_file_path)
                else:
                    error_feedback = "Manim reported successful compile, but output video file was not found."
                    current_retry += 1
            else:
                error_feedback = f"Error during Manim compilation:\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
                current_retry += 1
                print(f"Compilation error: {error_feedback}")
                
        except subprocess.TimeoutExpired:
            error_feedback = "Manim compilation timed out after 120 seconds."
            current_retry += 1
            print(error_feedback)
        except Exception as e:
            error_feedback = f"Unexpected subprocess error: {str(e)}"
            current_retry += 1
            print(error_feedback)

    raise RuntimeError(
        f"Failed to generate and render video after {max_retries} attempts.\n"
        f"Last Error details:\n{error_feedback}"
    )
