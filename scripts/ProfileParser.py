import json
import pandas as pd
from .__config import (
    EDUCATION_CSV,
    LANGUAGES_CSV,
    POSITIONS_CSV,
    PROFILE_CSV,
    PROJECTS_CSV,
    SKILLS_CSV, 
    logging
)

class ProfileParser:
    CSV_FILES = {
        'Education': EDUCATION_CSV,
        'Languages': LANGUAGES_CSV,
        'Positions': POSITIONS_CSV,
        'Profile': PROFILE_CSV,
        'Projects': PROJECTS_CSV,
        'Skills': SKILLS_CSV
    }

    data = {}
    parsed_data = {}
    structured_data = {}
    
    def __init__(self):
        
        self.load_all_data()
        self.parse_to_structured_data()
        self.restructured_data()
    
    def load_all_data(self):

        for name, filepath in self.CSV_FILES.items():
            if filepath.exists():
                self.data[name] = pd.read_csv(filepath)
                logging.info(f"Loaded {name}: {len(self.data[name])} records")
            else:
                logging.warning(f"File not found: {filepath}")

    def parse_to_structured_data(self):
        
        self.parsed_data = {
            'Education': self.data.get('Education', pd.DataFrame()).to_dict('records'),
            'Languages': self.data.get('Languages', pd.DataFrame()).to_dict('records'),
            'Positions': self.data.get('Positions', pd.DataFrame()).to_dict('records'),
            'Profile': self.data.get('Profile', pd.DataFrame()).to_dict('records'),
            'Projects': self.data.get('Projects', pd.DataFrame()).to_dict('records'),
            'Skills': self.data.get('Skills', pd.DataFrame()).to_dict('records')
        }

    def restructured_data(self):
        pass
    
if __name__ == "__main__":
    # Testing
    PP = ProfileParser()
    logging.info(json.dumps(PP.parsed_data, indent=2, ensure_ascii=False))