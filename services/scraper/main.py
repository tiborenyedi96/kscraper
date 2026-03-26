import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> dict[str, str] | None:
    page_limiter: int = 1
    keys: list[str] = []
    values: list[str] = []

    for i in range(1, page_limiter + 1):
        current_url: str = f"{url}/catalogue/page-{i}.html"
        try:
            request = requests.get(current_url)
        except Exception as e:
            print(e)
            return None

        if request.status_code != 200:
            break

        soup = BeautifulSoup(request.content.decode("utf-8"), features="html.parser")

        for item in soup.find_all("a"):
            if item.get("title"):
                keys.append(item.get("title"))

        for item in soup.find_all("p", {"class": "price_color"}):
            values.append(item.get_text().replace("£", ""))

    result = dict(zip(keys, values))
    return result


def main():
    result = scrape("https://books.toscrape.com")
    print(result)


if __name__ == "__main__":
    main()
