import os
import zipfile
from pathlib import Path
import pandas as pd
from .__config import INPUT_DIR, DATA_DIR, logging
import json


class ExtractCSV:

    _FILES_NAMES = [
        "profile.csv",
        "positions.csv",
        "skills.csv",
        "education.csv",
        "languages.csv",
        "projects.csv",
    ]

    _zip_path: Path = None

    def __init__(self, debug=False):
        self._debug = debug

        self._find_zip_file()
        self.data = self._get_data()

    def _find_zip_file(self) -> Path:

        self._zip_path = next(INPUT_DIR.glob("*.zip"), None)
        if self._zip_path:
            logging.info(f"Found ZIP: {self._zip_path}")
        else:
            logging.warning(f"No .zip file found in {INPUT_DIR.name}/")

    def _get_data(self):
        try:
            data = {}
            with zipfile.ZipFile(self._zip_path, "r") as zip_ref:

                all_files = zip_ref.namelist()

                for file in all_files:
                    file_name = os.path.basename(file).lower()
                    if file_name in self._FILES_NAMES:
                        try:
                            with zip_ref.open(file, "r") as f:
                                df = pd.read_csv(f)
                                # Replace NaN/NA with Python None for consistency
                                df = df.where(pd.notna(df), None)
                                name = file_name[:-4].capitalize()
                                data[name] = df.to_dict("records")
                                logging.info(f"✓ Loaded into memory: {file} -> {name}")

                            if self._debug:
                                zip_ref.extract(file, DATA_DIR)
                                logging.info(f"✓ Extracted: {file}")

                        except Exception as e:
                            logging.error(f"✗ Error extracting {file}: {e}")

        except zipfile.BadZipFile:
            logging.error("Error: ZIP file is corrupted or invalid.")
        except Exception:
            logging.error(f"Error: File {self._zip_path} not found.")
        finally:
            # delete file after extraction
            if self._zip_path and not self._debug:
                try:
                    os.remove(self._zip_path)
                    logging.info(f"Deleted ZIP file: {self._zip_path.name}")
                except OSError as e:
                    logging.warning(f"Could not delete ZIP file: {e}")
        return data


if __name__ == "__main__":
    # Testing
    ExtCSV = ExtractCSV(debug=True)
    print(json.dumps(ExtCSV.data, ensure_ascii=False, indent=2))
