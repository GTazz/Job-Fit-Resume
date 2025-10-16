import os
import zipfile
from pathlib import Path


class ExtractCSV:

    FILES_NAMES = [
        "profile.csv",
        "positions.csv",
        "skills.csv",
        "education.csv",
        "languages.csv",
        "projects.csv",
    ]

    DATA_DIR: Path = Path("data")
    zip_path: Path = None

    def __init__(self):
        pass

    def find_zip_file(self) -> Path:

        self.zip_path = next(self.DATA_DIR.glob("*.zip"), None)
        if self.zip_path:
            self.zip_path = self.zip_path  # Path is fine for zipfile.ZipFile
            print(f"Found ZIP: {self.zip_path}")
        else:
            print("No .zip file found in data/")

    def run(self):

        try:
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:

                all_files = zip_ref.namelist()

                for file in all_files:
                    file_name = os.path.basename(file).lower()
                    if file_name in self.FILES_NAMES:
                        try:
                            zip_ref.extract(file, self.DATA_DIR)
                            print(f"✓ Extracted: {file}")
                        except Exception as e:
                            print(f"✗ Error extracting {file}: {e}")

            # delete file after extraction
        except zipfile.BadZipFile:
            print("Error: ZIP file is corrupted or invalid.")
        except Exception:
            print(f"Error: File {self.zip_path} not found.")
        finally:
            if self.zip_path:
                os.remove(self.zip_path)


if __name__ == "__main__":
    # Testing
    ExtCSV = ExtractCSV()
    ExtCSV.find_zip_file()
    ExtCSV.run()
