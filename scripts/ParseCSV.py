import json
from .__config import (
    EDUCATION_CSV,
    LANGUAGES_CSV,
    POSITIONS_CSV,
    PROFILE_CSV,
    PROJECTS_CSV,
    SKILLS_CSV,
    PARSED_DATA_JSON,
    logging,
)


class ParseCSV:
    _CSV_FILES = {
        "Education": EDUCATION_CSV,
        "Languages": LANGUAGES_CSV,
        "Positions": POSITIONS_CSV,
        "Profile": PROFILE_CSV,
        "Projects": PROJECTS_CSV,
        "Skills": SKILLS_CSV,
    }

    # Desired fields per section (using itemgetter)
    _DESIRED_FIELDS = {
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

    def __init__(self, data: dict = None, debug: bool = False):
        self._debug = debug

        data = self._filter_data(data)
        self.data = self._parse_data(data)
        if self._debug:
            self._save_parsed_data()

    def _filter_data(self, data):
        self.filtered_data = {}
        for section, records in data.items():
            desired_fields = self._DESIRED_FIELDS.get(section)

            if desired_fields is True:
                self.filtered_data[section] = records
            else:
                # Extract only the desired fields
                self.filtered_data[section] = [
                    {field: record.get(field) for field in desired_fields}
                    for record in records
                ]

        return self.filtered_data

    def _parse_data(self, data):
        # Placeholder for any additional parsing logic
        return data
    
    def _save_parsed_data(self):
        try:
            with open(PARSED_DATA_JSON, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved parsed data to {PARSED_DATA_JSON}")
        except Exception as e:
            logging.error(f"Failed to save parsed data to {PARSED_DATA_JSON}: {e}")
            raise


if __name__ == "__main__":
    from .ExtractCSV import ExtractCSV
    debug = True
    
    # Testing
    E_CSV = ExtractCSV(debug=debug)
    P_CSV = ParseCSV(data=E_CSV.data, debug=debug)
