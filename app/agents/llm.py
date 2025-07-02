from agno.models import google
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Check if API key is available
if not settings.google_api_key:
    logger.error("Google API key not found! Please set google_api_key in .env file")
    chat_model = None
else:
    try:
        chat_model = google.Gemini(
            id="gemini-2.0-flash-001",
            api_key=settings.google_api_key,
            max_output_tokens=8192
        )
        logger.info("Gemini model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        chat_model = None
