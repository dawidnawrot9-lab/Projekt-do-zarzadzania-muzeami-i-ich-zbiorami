import requests
from bs4 import BeautifulSoup

def get_coordinates(lokalizacja: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{lokalizacja}"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except Exception:
        return [0.0, 0.0]