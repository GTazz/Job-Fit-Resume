import os
import logging
from dotenv import load_dotenv
import json
from copy import deepcopy
from openai import OpenAI, BadRequestError, AuthenticationError, RateLimitError

class TextGeneration():
    
    # Constant variables
    MODELS = [".1", ".1-mini", ".1-nano", "o", "o-mini"]
    PROMPT_FILENAME = "aiConfig.md"
    VARIABLES_FILENAME = "cv_variables.json"
    TEMPLATE_FILENAME = "template.docx"
        
    def __init__(self):

        # Variables declaration
        self.ai_raw_response = None  # Raw AI response

        # Sequential execution of steps
        self.setup()
        self.parse_cv_functions()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()
        self.step7()
        
    def setup(self):

        # Configure logging level as INFO
        logging.basicConfig(level=logging.INFO)
        
        # Loads environment variables of the .env file, overriding existing values, if necessary
        load_dotenv(override=True)

        # Get the AI API token stored as an environmental variable in the .env file
        AI_API_TOKEN = os.getenv("AI_API_TOKEN")

        endpoint = "https://models.github.ai/inference"

        self.current_model = self.MODELS[0]
        self.model = "openai/gpt-4" + self.current_model

        self.client = OpenAI(
            base_url=endpoint,
            api_key=AI_API_TOKEN,
        )

        with open(self.PROMPT_FILENAME, "r", encoding="utf-8") as file:
            self.SYS_PROMPT = file.read()

    def parse_cv_functions(self):
        pass
    
    def step2(self):
        pass

    def step3(self):
        pass

    def step4(self):
        pass

    def step5(self):
        pass

    def step6(self):
        pass

    def step7(self):
        pass



if __name__ == "__main__":
    TG = TextGeneration()
