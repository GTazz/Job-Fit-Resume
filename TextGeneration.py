import os
import logging
from dotenv import load_dotenv
import json
from copy import deepcopy
from openai import OpenAI, BadRequestError, AuthenticationError, RateLimitError
from openai.types.chat import ChatCompletionMessage


class TextGeneration:

    # Constant variables:
    MODELS: list[str] = [
        ".1",
        ".1-mini",
        ".1-nano",
        "o",
        "o-mini",
    ]  # Available model versions
    PROMPT_FILENAME: str = "aiConfig.md"  # System prompt file
    VARIABLES_FILENAME: str = "cv_variables_context.json"  # CV variables and context file
    VARIABLES_OUTPUT_FILENAME: str = "cv_variables.json"  # CV variables output file
    TEMPLATE_FILENAME: str = "template.docx"  # Resume template file

    # General variables declaration
    current_model: str = MODELS[0]  # Default model version
    model: str = "openai/gpt-4" + current_model  # Default model
    client: OpenAI = None  # OpenAI client
    user_prompt: str = None  # User prompt
    ai_raw_response: ChatCompletionMessage = None  # Raw AI response
    tools: list[dict] = None  # List of tools (functions) available to the AI

    def __init__(self):

        # Sequential execution of steps
        self.setup()
        self.parse_cv_functions()
        self.ai_request()
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

        self.client = OpenAI(
            base_url=endpoint,
            api_key=AI_API_TOKEN,
        )

        with open(self.PROMPT_FILENAME, "r", encoding="utf-8") as file:
            self.SYS_PROMPT = file.read()

    def parse_cv_functions(self):

        # Placeholder variables (work in progress)
        properties_names = ["mainStack"]
        
        properties = {
            "mainStack": {
                "type": "string",
                "description": "PLACEHOLDER",
            }
        },
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "CVTexts",
                    "description": "User Gives Job Description and Current Resume. AI must answer with improved resume texts.",
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": properties_names,
                    },
                },
            }
        ]

    def ai_request(self) -> None:
        logging.info("Using model %s", self.model)

        self.ai_raw_response = (
            self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.SYS_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": self.user_prompt,
                    },
                ],
                tools=self.tools,
                # always activate a function to combine the responses
                tool_choice={"type": "function", "function": {"name": "CVTexts"}},
                temperature=1,  # Grau de criatividade (quanto maior, mais criativo)
                top_p=1,  # Probabilidade acumulada para amostragem (nucleus sampling)
                model=self.model,  # Modelo escolhido
            )
            .choices[0]
            .message
        )

        self.process_request()

    def process_request(self):
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

    def _handle_rate_limit_error(self) -> None:
        try:
            logging.warning("%s model exceeded.", self.model)

            self.current_model = self.MODELS[self.MODELS.index(self.current_model) + 1]
            self.model = "openai/gpt-4" + self.current_model

            logging.warning("Changed to model %s.", self.model)

            self.ai_request()

        except IndexError:
            logging.error("All models have been exhausted.")


if __name__ == "__main__":
    TG = TextGeneration()
