import os
import zipfile
from pathlib import Path
from .__config import DATA_DIR, logging

class ExtractCSV:

    FILES_NAMES = [
        "profile.csv",
        "positions.csv",
        "skills.csv",
        "education.csv",
        "languages.csv",
        "projects.csv",
    ]

    zip_path: Path = None

    def __init__(self):
        pass

    def find_zip_file(self) -> Path:
        self.zip_path = next(DATA_DIR.glob("*.zip"), None)
        if self.zip_path:
            logging.info(f"Found ZIP: {self.zip_path}")
        else:
            logging.warning(f"No .zip file found in {DATA_DIR.name}/")

    def run(self):

        try:
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:

                all_files = zip_ref.namelist()

                for file in all_files:
                    file_name = os.path.basename(file).lower()
                    if file_name in self.FILES_NAMES:
                        try:
                            zip_ref.extract(file, DATA_DIR)
                            logging.info(f"✓ Extracted: {file}")
                        except Exception as e:
                            logging.error(f"✗ Error extracting {file}: {e}")

            # delete file after extraction
        except zipfile.BadZipFile:
            logging.error("Error: ZIP file is corrupted or invalid.")
        except Exception:
            logging.error(f"Error: File {self.zip_path} not found.")
        finally:
            if self.zip_path:
                os.remove(self.zip_path)


if __name__ == "__main__":
    # Testing
    ExtCSV = ExtractCSV()
    ExtCSV.find_zip_file()
    ExtCSV.run()
