import os
import logging
from dotenv import load_dotenv
import json
from openai import OpenAI, BadRequestError, AuthenticationError, RateLimitError


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
    user_prompt: str = ""  # User prompt
    _current_model: str = _MODELS[0]  # Default model version
    _model: str = "openai/gpt-4" + _current_model  # Default model
    _client: OpenAI = None  # OpenAI client
    _messages: list[dict[str, str]] = []  # List of messages (system + user)
    _tools: list[dict] = []  # List of tools (functions) available to the AI
    _processed_response: dict[str] = {}  # Raw AI response

    def __init__(self) -> None:

        # Configure logging level as INFO
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Loads .env file's environment variables, overriding existing values, if necessary
        load_dotenv(override=True)

        # Initialize OpenAI client
        self._client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("AI_API_TOKEN"),
        )
        
        logging.info("OpenAI client initialized.")

    def run(self, user_prompt: str = None) -> None:
        # Use the provided user prompt or the variable value
        self.user_prompt = self.user_prompt if user_prompt is None else user_prompt

        # Sequential execution of steps
        self.parse_prompt()
        self.parse_cv_functions()
        self.ai_request()
        self.save_json_output()

    def parse_prompt(self) -> None:

        with open(self._PROFILE_FILENAME, "r", encoding="utf-8") as file:
            sys_prompt = file.read()

            user_prompt = f"JOB DESCRIPTION:\n\n{self.user_prompt}"
            self._messages = [
                {
                    "role": "system",
                    "content": sys_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
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
                    "description": "Given a job description, generate tailored resume content highlighting only genuine qualifications from the candidate's profile that directly match the job requirements. Focus on the most essential and impactful alignments (never fabricate qualifications).",
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

            self._processed_response = json.loads(
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
                .message.tool_calls[0]
                .function.arguments
            )
        
            logging.info("AI response processed successfully.")
            logging.info("Generated CV Variables:\n%s", json.dumps(self._processed_response, indent=4, ensure_ascii=False))

        except RateLimitError:
            self._handle_rate_limit_error()

    def save_json_output(self) -> None:
        with open(self._VARIABLES_OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            json.dump(self._processed_response, file, indent=4, ensure_ascii=False)
        
        logging.info("CV variables saved to %s", self._VARIABLES_OUTPUT_FILENAME)

    def _handle_rate_limit_error(self) -> None:
        try:
            logging.warning("%s model exceeded.", self._model)

            self._current_model = self._MODELS[
                self._MODELS.index(self._current_model) + 1
            ]
            self._model = "openai/gpt-4" + self._current_model

            logging.warning("Changed to model %s.", self._model)

            self.ai_request()

        except IndexError:
            logging.error("All models have been exhausted.")


if __name__ == "__main__":
    TG = TextGeneration()
    TG.user_prompt = """
Sobre a vaga

Required Qualifications:

    Bachelor’s or Master’s degree in Data Science, Computer Science, Statistics, or a related field.
    3+ years of experience building and deploying ML models in enterprise environments.
    Proficiency in PySpark, Python, and ML frameworks (e.g., scikit-learn, TensorFlow, PyTorch).
    Hands-on experience with Databricks, Azure ML, AWS SageMaker, or Google Vertex AI.
    Strong coding skills and experience with scalable data workflows and model deployment.
    Familiarity with GenAI, LLMs, and NLP techniques.
    Ability to work independently and manage priorities in a fast-paced environment.
    Availability to support meetings or calls outside standard working hours as needed.

 

 

Preferred Skills:

    Experience with time-series demand forecasting, margin-aware modeling, text summarization, and stock-based recommendations.
    Exposure to multi-modal data and personalization strategies across digital ecosystems.


We are seeking a highly capable Data Scientist to help build and scale enterprise-grade AI/ML products within our centralized Data Science team. This role focuses on developing intelligent, production-ready solutions that power personalization, forecasting, and automation across our digital platforms. The ideal candidate is a strong problem-solver, able to work independently, and comfortable supporting collaboration across time zones—including occasional calls outside standard working hours.
"""
    TG.run()
