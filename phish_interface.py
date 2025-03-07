import logging
from difflib import unified_diff

import requests
from openai import OpenAI

from james_linkedin import PAGE as PAGE_JAMES
from jeremy_linkedin import PAGE as PAGE_JEREMY

logger = logging.getLogger(__name__)
client = OpenAI()

# System prompt for generating marketing email from HTML content
MAKE_EMAIL_RESPONSE = """
The user will provide a corporate webpage in HTML. Respond with an HTML marketing email inspired by the page. Use a similar communication strategy.
"""


def get_email_html(homepage_html: str) -> str:
    """Generates a marketing email HTML from a given corporate webpage HTML."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": MAKE_EMAIL_RESPONSE},
                {"role": "user", "content": homepage_html},
            ],
            response_format={"type": "text"},
            temperature=1,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to generate email HTML: {e}")
        return ""


def request_linkedin_html(url: str) -> str:
    """Logs differences between two predefined LinkedIn pages."""
    diff = "\n".join(unified_diff(PAGE_JAMES, PAGE_JEREMY))
    if diff:
        logger.warning(f"LinkedIn Page Diff:\n{diff}")
    return diff
