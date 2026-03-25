import requests
from bs4 import BeautifulSoup

def main():
    try:
        request = requests.get("https://books.toscrape.com/")
    except Exception as e:
        print (e)
        return None

    soup = BeautifulSoup(request.content.decode("utf-8"), features="html.parser")
    
    # getting the book titles
    book_titles: list[str] = []
    for item in soup.find_all("a"):
        if item.get("title"):
            book_titles.append(item.get("title"))

    # getting the book prices
    book_prices: list[str] = []
    for item in soup.find_all("p", {"class": "price_color"}):    
        book_prices.append(item.get_text().replace("£", ""))
    
    # merge them together
    books: list[str] = []
    try:
        for i in range(len(book_titles)):
            books.append(book_titles[i])
            books.append(book_prices[i])
    except IndexError as e:
        print(e)
        return None
    
    print(books)

if __name__ == "__main__":
    main()