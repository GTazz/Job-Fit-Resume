import json
import pandas as pd
from pathlib import Path

class ProfileParser:
    DATA_DIR = Path("linkedin_data")
    CSV_FILES = {
        'Education': DATA_DIR / 'Education.csv',
        'Languages': DATA_DIR / 'Languages.csv',
        'Positions': DATA_DIR / 'Positions.csv',
        'Profile': DATA_DIR / 'Profile.csv',
        'Projects': DATA_DIR / 'Projects.csv',
        'Skills': DATA_DIR / 'Skills.csv'
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
            'Education': self.data.get('Education', pd.DataFrame()).to_dict('records'),
            'Languages': self.data.get('Languages', pd.DataFrame()).to_dict('records'),
            'Positions': self.data.get('Positions', pd.DataFrame()).to_dict('records'),
            'Profile': self.data.get('Profile', pd.DataFrame()).to_dict('records'),
            'Projects': self.data.get('Projects', pd.DataFrame()).to_dict('records'),
            'Skills': self.data.get('Skills', pd.DataFrame()).to_dict('records')
        }
        
    
if __name__ == "__main__":
    PP = ProfileParser()
    print(json.dumps(PP.parsed_data, indent=2, ensure_ascii=False))