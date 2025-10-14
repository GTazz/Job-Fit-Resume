import os
import zipfile
from pathlib import Path


class ExtractCSV:

    DATA_DIR = Path("linkedin_data")
    FILES_NAMES = [
        "profile.csv",
        "positions.csv",
        "skills.csv",
        "education.csv",
        "languages.csv",
        "projects.csv",
    ]

    zip_file_name: str = ""

    def __init__(self, zip_file_name: str = None):
        self.zip_file_name = self.zip_file_name if zip_file_name is None else zip_file_name

    def run(self):

        os.makedirs(self.DATA_DIR, exist_ok=True)

        try:
            with zipfile.ZipFile(self.zip_file_name, "r") as zip_ref:

                all_files = zip_ref.namelist()

                for file in all_files:
                    file_name = os.path.basename(file).lower()
                    if file_name in self.FILES_NAMES:
                        try:
                            zip_ref.extract(file, self.DATA_DIR)
                            print(f"✓ Extracted: {file}")
                        except Exception as e:
                            print(f"✗ Error extracting {file}: {e}")

        except zipfile.BadZipFile:
            print("Error: ZIP file is corrupted or invalid.")
        except FileNotFoundError:
            print(f"Error: File {self.zip_file_name} not found.")

if __name__ == "__main__":
    ExtCSV = ExtractCSV()
    
    ExtCSV.zip_file_name = "Basic_LinkedInDataExport_10-12-2025.zip.zip"

    ExtCSV.run()
