import json
import pandas as pd
from operator import itemgetter
from .__config import (
    EDUCATION_CSV,
    LANGUAGES_CSV,
    POSITIONS_CSV,
    PROFILE_CSV,
    PROJECTS_CSV,
    SKILLS_CSV,
    logging,
)


class ProfileParser:
    CSV_FILES = {
        "Education": EDUCATION_CSV,
        "Languages": LANGUAGES_CSV,
        "Positions": POSITIONS_CSV,
        "Profile": PROFILE_CSV,
        "Projects": PROJECTS_CSV,
        "Skills": SKILLS_CSV,
    }

    # Desired fields per section (using itemgetter)
    DESIRED_FIELDS = {
        "Education": [
            "School Name",
            "Start Date",
            "End Date",
            "Degree Name",
            "Activities",
        ],
        "Languages": ["Name", "Proficiency"],
        "Positions": [
            "Company Name",
            "Title",
            "Description",
            "Location",
            "Started On",
            "Finished On",
        ],
        "Projects": ["Title", "Description", "Url", "Started On", "Finished On"],
        "Skills": ["Name"],
        "Profile": True,  # True = keep all fields
    }

    data = {}
    parsed_data = {}
    filtered_data = {}

    def __init__(self):

        self.load_all_data()
        self.parse_to_structured_data()
        self.filter_data()

    def load_all_data(self):

        for name, filepath in self.CSV_FILES.items():
            if filepath.exists():
                self.data[name] = pd.read_csv(filepath)
                logging.info(f"Loaded {name}: {len(self.data[name])} records")
            else:
                logging.warning(f"File not found: {filepath}")

    def parse_to_structured_data(self):

        self.parsed_data = {
            "Education": self.data.get("Education", pd.DataFrame()).to_dict("records"),
            "Languages": self.data.get("Languages", pd.DataFrame()).to_dict("records"),
            "Positions": self.data.get("Positions", pd.DataFrame()).to_dict("records"),
            "Profile": self.data.get("Profile", pd.DataFrame()).to_dict("records"),
            "Projects": self.data.get("Projects", pd.DataFrame()).to_dict("records"),
            "Skills": self.data.get("Skills", pd.DataFrame()).to_dict("records"),
        }

    def filter_data(self):
        for section, records in self.parsed_data.items():
            desired_fields = self.DESIRED_FIELDS.get(section)

            if desired_fields is True:
                self.filtered_data[section] = records
            else:
                # Use itemgetter to extract only the desired fields
                try:
                    getter = itemgetter(*desired_fields)
                    self.filtered_data[section] = [
                        {
                            field: value
                            for field, value in zip(
                                desired_fields,
                                (
                                    getter(record)
                                    if len(desired_fields) > 1
                                    else [getter(record)]
                                ),
                            )
                        }
                        for record in records
                        if all(
                            field in record for field in desired_fields
                        )
                        
                    ]
                except KeyError:
                    logging.warning(
                        f"Some fields not found in {section}, using fallback"
                    )
                    self.filtered_data[section] = records


if __name__ == "__main__":
    # Testing
    PP = ProfileParser()
    logging.info(json.dumps(PP.filtered_data, indent=2, ensure_ascii=False))
