import requests
from bs4 import BeautifulSoup


def fetch_news(url="https://news.ycombinator.com/"):
    """Fetch Hacker News homepage HTML and parse with BeautifulSoup."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def popular_news(links, votes, min_points=100):
    """
    Extract popular news articles from Hacker News.

    Args:
        links (list): List of link elements containing news titles and href.
        votes (list): List of vote elements containing points.
        min_points (int): Minimum number of points required to include news.

    Returns:
        list[dict]: A list of dictionaries with title, href, and points.
    """
    popular = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)

        try:
            points = int(votes[idx].getText().replace(" points", "").strip())
        except (IndexError, ValueError):
            points = 0

        if points >= min_points:
            popular.append({
                "title": title,
                "href": href,
                "points": points
            })

    return popular


if __name__ == "__main__":
    soup = fetch_news()
    links = soup.select(".titleline a")
    votes = soup.select(".score")

    news = popular_news(links, votes, min_points=100)

    print("\n🔥 Popular Hacker News Articles 🔥\n")
    for n in news:
        print(f"📌 {n['title']} ({n['points']} points)")
        print(f"👉 {n['href']}\n")
