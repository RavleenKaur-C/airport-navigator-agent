import requests
from bs4 import BeautifulSoup
from typing import Optional

def get_airport_wikivoyage_text(airport_name: str) -> Optional[str]:

    """
    Fetches the Wikivoyage page text for a given airport.
    E.g., airport_name="London Heathrow" → https://en.wikivoyage.org/wiki/London_Heathrow_Airport
    """
    formatted_name = airport_name.strip().replace(" ", "_")
    url = f"https://en.wikivoyage.org/wiki/{formatted_name}_Airport"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[!] Page not found: {url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove navbars and tables
    for tag in soup.find_all(["table", "nav", "style", "script"]):
        tag.decompose()

    # Just get the main text content
    paragraphs = soup.find_all("p")
    text = "\n".join(p.get_text() for p in paragraphs)
    return text.strip()
