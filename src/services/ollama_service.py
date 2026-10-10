
import requests
from loguru import logger

from configs import settings


def generate_summary(text: str, title: str = "Research paper") -> str:
    """Generate a concise paper summary using local Ollama."""

    if not text or not text.strip():
        logger.warning("No source text available for paper: {}", title)
        return "Summary unavailable: no paper text or abstract was provided."

    # Limit input size to avoid very slow inference.
    source_text = text[:6000]

    prompt = f"""
You are an academic research assistant.

Summarize the following research paper using only the supplied text.
Do not invent results, metrics, or conclusions.

Paper title: {title}

Provide:
1. Research problem
2. Methodology
3. Main contributions
4. Findings and limitations, if stated

Keep the summary concise, around 150 words.

Paper content:
{source_text}
"""

    url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "num_predict": 256,
            "temperature": 0.2,
            "num_ctx": 4096,
        },
    }

    try:
        logger.info("Requesting Ollama summary for: {}", title)

        response = requests.post(
            url,
            json=payload,
            timeout=(10, 300),
        )
        response.raise_for_status()

        summary = response.json().get("response", "").strip()

        if not summary:
            logger.warning("Ollama returned an empty summary for: {}", title)
            return "Summary unavailable: Ollama returned an empty response."

        logger.info("Successfully summarized: {}", title)
        return summary

    except requests.RequestException as exc:
        logger.error("Ollama request failed for '{}': {}", title, exc)
        return (
            "Summary generation failed because the local Ollama service "
            "did not return a usable response. "
            "Refer to the paper abstract for details."
        )
    except (ValueError, KeyError) as exc:
        logger.error("Invalid Ollama response for '{}': {}", title, exc)
        return "Summary unavailable: invalid response from Ollama."
