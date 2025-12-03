import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# ==== PATHS ====

# Directories
DATA_DIR = Path("data")
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
TEMPLATES_DIR = Path("templates")
TEMP_DIR = Path("temp")

# Files - ParseCSV
EDUCATION_CSV = DATA_DIR / "Education.csv"
LANGUAGES_CSV = DATA_DIR / "Languages.csv"
POSITIONS_CSV = DATA_DIR / "Positions.csv"
PROFILE_CSV = DATA_DIR / "Profile.csv"
PROJECTS_CSV = DATA_DIR / "Projects.csv"
SKILLS_CSV = DATA_DIR / "Skills.csv"
PARSED_DATA_JSON = DATA_DIR / "profile.json"

# Files - BuildProfile
PROFILE_TEMPLATE_MD = TEMPLATES_DIR / "profile_template.md"

# Files - BuildProfile / GenerateAIText
PROFILE_MD = DATA_DIR / "profile.md"

# Files - GenerateAIText
CV_VARIABLES_CONTEXT_JSON = TEMPLATES_DIR / "template.json"

# Files - GenerateAIText / JsonToCurriculum
CV_VARIABLES_JSON = OUTPUT_DIR / "final_cv.json"

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
