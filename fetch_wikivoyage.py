import requests
from bs4 import BeautifulSoup

WIKIVOYAGE_BASE_URL = "https://en.wikivoyage.org/wiki/"

def fetch_wikivoyage_page(title: str) -> str or None:
    """
    Fetches and returns visible text content from a Wikivoyage page.
    Returns None if the page doesn't exist or has no extractable content.
    """
    url = WIKIVOYAGE_BASE_URL + title.replace(" ", "_")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[!] Page not found: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    return content.get_text(separator="\n") if content else None


def fetch_airport_text(name: str) -> str or None:
    """
    Tries fetching Wikivoyage text by:
    1. Full airport name
    2. Fallback to the first word (usually city)
    """
    name = name.replace("’", "").replace("'", "")
    main_query = name.replace(" ", "_")
    fallback_query = name.split()[0].replace(" ", "_")

    text = fetch_wikivoyage_page(main_query)
    if text:
        return text

    return fetch_wikivoyage_page(fallback_query)
