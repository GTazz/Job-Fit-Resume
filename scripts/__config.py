import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# ==== PATHS ====

# Directories
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
TEMPLATES_DIR = Path("templates")
TEMP_DIR = Path("temp")

# Files - ProfileParser
EDUCATION_CSV = DATA_DIR / "Education.csv"
LANGUAGES_CSV = DATA_DIR / "Languages.csv"
POSITIONS_CSV = DATA_DIR / "Positions.csv"
PROFILE_CSV = DATA_DIR / "Profile.csv"
PROJECTS_CSV = DATA_DIR / "Projects.csv"
SKILLS_CSV = DATA_DIR / "Skills.csv"

# Files - ProfileBuilder / TextGeneration
PROFILE_MD = DATA_DIR / "profile.md"

# Files - TextGeneration
CV_VARIABLES_CONTEXT_JSON = TEMPLATES_DIR / "cv_variables_context.json"

# Files - TextGeneration / JsonToCurriculum
CV_VARIABLES_JSON = DATA_DIR / "cv_variables.json"

# Files - JsonToCurriculum
TEMPLATE_DOCX = TEMPLATES_DIR / "template.docx"
FINAL_CV_DOCX = OUTPUT_DIR / "final_cv.docx"
FINAL_CV_PDF = OUTPUT_DIR / "final_cv.pdf"


# ==== LOGGING ====
    
# Configure logging level as INFO
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==== LOAD .env ====

# Loads .env file's environment variables, overriding existing values, if necessary
load_dotenv(override=True)

# OpenAI API token
AI_API_TOKEN = os.getenv("AI_API_TOKEN")
