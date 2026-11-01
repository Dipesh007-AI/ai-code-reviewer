import os
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "api key not found"
    )
    
    
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

CHAT_MODEL = "openrouter/free"
