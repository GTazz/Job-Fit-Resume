import json
import pandas as pd
from .__config import (
    EDUCATION_CSV,
    LANGUAGES_CSV,
    POSITIONS_CSV,
    PROFILE_CSV,
    PROJECTS_CSV,
    SKILLS_CSV,
    logging,
)


class ParseCSV:
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
        "Languages": True,  # True = keep all fields
        "Positions": [
            "Company Name",
            "Title",
            "Description",
            "Started On",
            "Finished On",
        ],
        "Projects": ["Title", "Description"],
        "Skills": True,
        "Profile": ["First Name", "Last Name", "Headline", "Summary"],
    }

    def __init__(self):

        data = self.load_all_data()
        data = self.filter_data(data)
        self.parsed_data = self.parse_data(data)

    def load_all_data(self):
        data = {}
        for name, filepath in self.CSV_FILES.items():
            if filepath.exists():
                data[name] = pd.read_csv(filepath).to_dict("records")
                logging.info(f"Loaded {name}: {len(data[name])} records")
            else:
                logging.warning(f"File not found: {filepath}")
        return data

    def filter_data(self, data):
        self.filtered_data = {}
        for section, records in data.items():
            desired_fields = self.DESIRED_FIELDS.get(section)

            if desired_fields is True:
                self.filtered_data[section] = records
            else:
                # Extract only the desired fields
                self.filtered_data[section] = [
                    {field: record.get(field) for field in desired_fields}
                    for record in records
                ]

        return self.filtered_data

    def parse_data(self, data):
        # Placeholder for any additional parsing logic
        return data


if __name__ == "__main__":
    # Testing
    P_CSV = ParseCSV()
    logging.info(json.dumps(P_CSV.parsed_data, indent=2, ensure_ascii=False))
