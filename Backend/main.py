import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from log_color_Formatter import ColorFormatter

# ------------------ Logging ------------------
def configure_terminal_logger():
    """Configure a console logger with color formatting."""
    logging.getLogger().handlers.clear()
    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(console_handler)

    # Nettoyer les logs de certains packages bruyants
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "werkzeug", "asyncio"]:
        logging.getLogger(name).handlers.clear()

configure_terminal_logger()
logger = logging.getLogger(__name__)

# ------------------ Load .env ------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
logger.info("Loaded .env variables")

# ------------------ LLM ------------------
logger.info("Initializing LLM...")
llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    model="deepseek-ai/deepseek-v3.1",
    temperature=0
)
logger.info("LLM initialized successfully")

# ------------------ Fonction utilitaire ------------------
def generate_response(prompt_text: str) -> str:
    """
    Génère une réponse à partir du LLM pour un texte donné.
    """
    from langchain_core.messages import HumanMessage

    logger.info("Generating response for input")
    response_obj = llm.generate([[HumanMessage(content=prompt_text)]])
    response_text = response_obj.generations[0][0].text
    logger.info("Response generated successfully")
    return response_text
