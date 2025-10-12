import json
import pandas as pd
from pathlib import Path

class ProfileParser:
    DATA_DIR = Path("data")
    CSV_FILES = {
        'education': DATA_DIR / 'Education.csv',
        'languages': DATA_DIR / 'Languages.csv',
        'positions': DATA_DIR / 'Positions.csv',
        'profile': DATA_DIR / 'Profile.csv',
        'projects': DATA_DIR / 'Projects.csv',
        'skills': DATA_DIR / 'Skills.csv'
    }
        
    data = {}
    
    def __init__(self):
        self.load_all_data()
        self.parse_to_structured_data()
    
    def load_all_data(self):

        for name, filepath in self.CSV_FILES.items():
            if filepath.exists():
                self.data[name] = pd.read_csv(filepath)
                print(f"Loaded {name}: {len(self.data[name])} records")
            else:
                print(f"File not found: {filepath}")
    
    def parse_to_structured_data(self):
        
        self.parsed_data = {
            'personal_info': self.data.get('profile', pd.DataFrame()).to_dict('records'),
            'experience': self.data.get('positions', pd.DataFrame()).to_dict('records'),
            'education': self.data.get('education', pd.DataFrame()).to_dict('records'),
            'skills': self.data.get('skills', pd.DataFrame()).to_dict('records'),
            'projects': self.data.get('projects', pd.DataFrame()).to_dict('records'),
            'languages': self.data.get('languages', pd.DataFrame()).to_dict('records')
        }
        
    
if __name__ == "__main__":
    PP = ProfileParser()
    print(json.dumps(PP.parsed_data, indent=2, ensure_ascii=False))