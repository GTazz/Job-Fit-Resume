import os
import logging
from dotenv import load_dotenv
import json
from openai import OpenAI, BadRequestError, AuthenticationError, RateLimitError
from openai.types.chat import ChatCompletionMessage


class TextGeneration:

    # Constant variables:
    _MODELS: list[str] = [
        ".1",
        ".1-mini",
        ".1-nano",
        "o",
        "o-mini",
    ]  # Available model versions
    _PROFILE_FILENAME: str = "profile.md"  # System prompt file
    _VARIABLES_FILENAME: str = "cv_variables_context.json"  # CV variables and context file
    _VARIABLES_OUTPUT_FILENAME: str = "cv_variables.json"  # CV variables output file
    _TEMPLATE_FILENAME: str = "template.docx"  # Resume template file

    # General variables declaration
    user_prompt: str = None  # User prompt
    _current_model: str = _MODELS[0]  # Default model version
    _model: str = "openai/gpt-4" + _current_model  # Default model
    _client: OpenAI = None  # OpenAI client
    _messages: list[dict[str, str]] = None  # List of messages (system + user)
    _tools: list[dict] = None  # List of tools (functions) available to the AI
    _ai_raw_response: ChatCompletionMessage = None  # Raw AI response

    def __init__(self) -> None:
        
        # Configure logging level as INFO
        logging.basicConfig(level=logging.INFO)

        # Loads environment variables of the .env file, overriding existing values, if necessary
        load_dotenv(override=True)

        self._client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("AI_API_TOKEN"),
        )

    def run(self, user_prompt: str = None) -> None:
        self.user_prompt = self.user_prompt if user_prompt is None else user_prompt

        # Sequential execution of steps
        self.parse_prompt()
        self.parse_cv_functions()
        self.ai_request()
        self.process_request()

    def parse_prompt(self) -> None:
        
        with open(self._PROFILE_FILENAME, "r", encoding="utf-8") as file:
            sys_prompt = file.read()
            
            
            self._messages = [
                {
                    "role": "system",
                    "content": sys_prompt,
                },
                {
                    "role": "user",
                    "content": self.user_prompt,
                },
            ]

    def parse_cv_functions(self) -> None:

        with open(self._VARIABLES_FILENAME, "r", encoding="utf-8") as file:
            raw_cv_variables = json.load(file)

        properties: dict = {}
        properties_names: list[str] = []
        for var, context in raw_cv_variables.items():
            properties[var] = {
                    "type": "string",
                    "description": context,
                }
            properties_names.append(var)
        
        self._tools = [
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
        try:
            logging.info("Using model %s", self._model)

            self._ai_raw_response = (
                self._client.chat.completions.create(
                    messages=self._messages,
                    tools=self._tools,
                    # always activate a function to combine the responses
                    tool_choice={"type": "function", "function": {"name": "CVTexts"}},
                    temperature=1,  # Grau de criatividade (quanto maior, mais criativo)
                    top_p=1,  # Probabilidade acumulada para amostragem (nucleus sampling)
                    model=self._model,  # Modelo escolhido
                )
                .choices[0]
                .message
            )
            
        except RateLimitError:
            self._handle_rate_limit_error()
     
    def process_request(self) -> None:
        pass

    def _handle_rate_limit_error(self) -> None:
        try:
            logging.warning("%s model exceeded.", self._model)

            self._current_model = self._MODELS[self._MODELS.index(self._current_model) + 1]
            self._model = "openai/gpt-4" + self._current_model

            logging.warning("Changed to model %s.", self._model)

            self.ai_request()

        except IndexError:
            logging.error("All models have been exhausted.")


if __name__ == "__main__":
    TG = TextGeneration()
    TG.user_prompt = "placeholder user prompt"
    TG.run()

