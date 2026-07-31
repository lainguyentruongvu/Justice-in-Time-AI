"""Quick Gemini connection test. Run: py test_gemini.py"""

from __future__ import annotations

from engine.config import GEMINI_API_KEY, MODEL


def main() -> None:
    api_key = str(GEMINI_API_KEY or "").strip().strip('"').strip("'")

    if not api_key:
        raise SystemExit(
            "Không đọc được GEMINI_API_KEY. Hãy kiểm tra file .env."
        )

    # Chỉ hiện một phần nhỏ, không làm lộ toàn bộ key
    print(f"Key đã đọc: {api_key[:3]}...{api_key[-4:]}")
    print(f"Độ dài key: {len(api_key)}")
    print(f"Model: {MODEL}")

    try:
        from google import genai
        from google.genai import errors
    except ImportError as exc:
        raise SystemExit(
            "Chưa cài google-genai. Chạy:\n"
            "py -m pip install --upgrade google-genai"
        ) from exc

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents="Reply with exactly: Gemini connection successful",
        )

        print(response.text or "Gemini returned an empty response.")

    except errors.ClientError as exc:
        raise SystemExit(f"Gemini API error:\n{exc}") from exc

    except Exception as exc:
        raise SystemExit(f"Gemini request failed:\n{exc}") from exc

    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()


if __name__ == "__main__":
    main()