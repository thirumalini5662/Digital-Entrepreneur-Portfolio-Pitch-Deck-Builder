import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def generate_ai_content(
    content_type,
    startup_name,
    industry,
    content
):

    if not client:
        return (
            "⚠️ Gemini API key not configured.\n\n"
            "Please add GEMINI_API_KEY to your .env file."
        )

    prompt = f"""
You are an expert startup consultant and pitch-deck content writer.

Startup Name: {startup_name}
Industry: {industry}

Content Type:
{content_type}

Original Startup Content:
{content}

Improve this content for a professional investor-ready
startup portfolio and pitch deck.

Rules:
- Keep the original meaning.
- Keep it concise.
- Use professional business language.
- Do not invent statistics.
- Do not invent financial figures.
- Do not invent customers or achievements.
- Return only the improved content.
"""

    # Try up to 3 times if Gemini is temporarily unavailable
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(3)
                    continue

                return (
                    "⚠️ Gemini is temporarily experiencing "
                    "high demand.\n\n"
                    "Please wait a few seconds and click "
                    "Generate AI Content again."
                )

            return (
                "❌ Gemini AI generation error:\n\n"
                f"{error_text}"
            )

    return "⚠️ AI service temporarily unavailable."