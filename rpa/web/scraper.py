from rpa.utils.fetch import fetch_page
from rpa.utils.get_dates import get_search_dates
from rpa.utils.parse import parse_data


def scrape_recent_acts() -> list[dict]:
    all_acts = []

    for search_date in get_search_dates():
        html = fetch_page(search_date)
        all_acts.extend(parse_data(html))

    return all_acts


def run_scraper() -> list[dict]:
    return scrape_recent_acts()