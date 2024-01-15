import requests
from bs4 import BeautifulSoup


def scrape_eco(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        eco_code = url.split("/")[-1]  # Extract ECO code from the URL

        h1_tag = soup.find("h1")
        title = h1_tag.text if h1_tag else "Title not found"

        return f"ECO Code: {eco_code}, Title: {title}"
    else:
        return f"Error: Unable to fetch content from {url}"


def extractOpening(input_string):
    parts = input_string.split(",")
    title_part = next((part.strip() for part in parts if "Title:" in part), None)
    title = title_part.split(":", 1)[1].strip() if title_part else None
    return title
