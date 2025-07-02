from agno.models import google
from app.config import settings

chat_model = google.Gemini(id="gemini-2.0-flash-001",api_key=settings.google_api_key,max_output_tokens=8192)
