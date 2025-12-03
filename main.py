from src import GenerateAIText, JsonToCurriculum

if __name__ == "__main__":
    Gen_AI = GenerateAIText()
    Gen_AI.user_prompt = """
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
    Gen_AI.run()
    JsonToCurriculum(Gen_AI.ai_response, debug=True)
