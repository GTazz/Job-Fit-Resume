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
        "Languages": True,  # True = keep all fields
        "Education": True,
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
        self.data = self._flatten_data(data)
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

    def _flatten_data(self, data):

        # Combine First Name and Last Name into Full Name
        data["Profile"][0]["Full Name"] = f"{data['Profile'][0].pop("First Name")} {data["Profile"][0].pop("Last Name", "")}".strip()

        # Flatten Languages into "Name | Proficiency"
        if languages := data.get("Languages", None):
            for i, language in enumerate(languages):
                languages[i] = language.get("Name")
                if proficiency := language.get("Proficiency", None):
                    languages[i] += " | " + proficiency

        # Combine start and end date into 'Duration' for Positions and Education
        for field in (
            ("Positions", "Started On", "Finished On"),
            ("Education", "Start Date", "End Date"),
        ):
            if positions := data.get(field[0], None):
                for position in positions:
                    start = position.pop(field[1], "N/A")
                    finish = position.pop(field[2], "N/A")

                    if start != "N/A" and finish != "N/A":
                        position["Duration"] = f"{start} - {finish}"
                    elif start == "N/A":
                        position["Duration"] = "N/A"
                    else:
                        position["Duration"] = f"{start} - Present"

        # Flatten Skills into a list of skill names
        data["Skills"] = [
            skill.get("Name", []) for skill in data.get("Skills", []) if skill
        ]

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
