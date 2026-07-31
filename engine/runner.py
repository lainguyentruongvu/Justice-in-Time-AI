from __future__ import annotations

from .config import GEMINI_API_KEY, MAX_OUTPUT_TOKENS, MODEL, TEMPERATURE


class RunnerError(RuntimeError):
    """A user-friendly error raised when the Gemini request cannot complete."""


def _friendly_error(exc: Exception) -> str:
    message = str(exc)
    lower = message.lower()

    if "api key" in lower and ("invalid" in lower or "not valid" in lower):
        return "GEMINI_API_KEY is invalid. Create a new key in Google AI Studio and update the .env file."
    if "quota" in lower or "resource_exhausted" in lower or "429" in lower:
        return (
            "Gemini quota has been exceeded. Check your Gemini API usage, rate limits, "
            "and billing/project settings in Google AI Studio or Google Cloud."
        )
    if "permission" in lower or "403" in lower:
        return "The Gemini API key does not have permission to use this model or project."
    if "not found" in lower and "model" in lower:
        return "The selected Gemini model was not found. Check GEMINI_MODEL in the .env file."
    if "timeout" in lower or "timed out" in lower:
        return "The Gemini request timed out. Please try again."
    return f"Gemini request failed: {message}"


def run(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """Generate text with the official Google Gen AI Python SDK."""
    if not GEMINI_API_KEY:
        raise RunnerError("GEMINI_API_KEY is missing. Add it to the .env file.")
    if not user_prompt.strip():
        raise RunnerError("User input cannot be empty.")

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RunnerError(
            "The google-genai package is not installed. Run: py -m pip install -r requirements.txt"
        ) from exc

    selected_model = (model or MODEL).strip()
    if not selected_model:
        raise RunnerError("GEMINI_MODEL cannot be empty.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model=selected_model,
            contents=user_prompt.strip(),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            ),
        )
    except Exception as exc:
        raise RunnerError(_friendly_error(exc)) from exc
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()

    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise RunnerError(
            "Gemini returned no text. The response may have been blocked by safety filters or stopped early."
        )
    return text.strip()
