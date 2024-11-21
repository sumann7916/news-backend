import logging
from .base_scraper import BaseScraper
from news.models import NewsCreator, News, NewsCategory
from typing import List
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pytz
from summarizer.summarize import summarize

# Configure loggings
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

VALID_TIME = 24  # 1 hour
NPT = pytz.timezone("Asia/Kathmandu")


class MyRepublicaScraper(BaseScraper):
    name = "My Republica"
    base_url = NewsCreator.objects.get(name=name).url
    categories_to_scrap = ["politics", "sports", "society", "economy", "lifestyle"]
    creator = NewsCreator.objects.get(name=name)

    def scrap(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        for category in self.categories_to_scrap:
            url = f"{self.base_url}/category/{category}"
            logging.info(f"Scraping category: {category} from {url}")
            soup = self.fetch_articles(url, headers)

            if soup:
                articles = self.extract_articles(soup)
                logging.info(f"Found {len(articles)} articles in category: {category}")
                for link, time_str in articles:
                    parsed_time = self.parse_time(time_str)
                    if parsed_time and self.check_if_valid_time(parsed_time):
                        full_soup = self.scrape_full_article(link, headers)
                        if full_soup:
                            main_heading, content, image = self.extract_article_details(
                                full_soup
                            )
                            logging.info(f"Main Heading: {main_heading}")
                            # Call save_to_db to store the article
                            self.save_to_db(
                                main_heading,
                                content,
                                link,
                                image,
                                category,
                                parsed_time,
                            )
                    else:
                        logging.warning(
                            f"Article at {link} is not within valid time frame."
                        )

    def save_to_db(
        self,
        title: str,
        content: str,
        original_link: str,
        image_link: str,
        categoryName: str,
        published_at: datetime,
    ) -> None:
        try:

            category = NewsCategory.objects.get_or_create(name=categoryName.lower())[0]
            summary = summarize(content)
            news = News(
                title=title,
                summary=summary,
                category=category,
                creator=self.creator,
                original_link=original_link,
                image_link=image_link,
                published_at=published_at,
            )
            news.save()
        except Exception as e:
            logging.error(f"Error saving to database: {e}")
            print(f"Error saving to database: {e}")

    ## Helpers

    def parse_time(self, full_text: str):
        # Try to find the date substring directly
        start_index = full_text.find("Published On: ") + len("Published On: ")
        end_index = full_text.find(" NPT")
        if start_index == -1 or end_index == -1:
            logging.error("Date format not found.")
            return None
        date_str = full_text[start_index:end_index].strip()
        date_format = "%B %d, %Y %I:%M %p"
        try:
            dt = datetime.strptime(date_str, date_format)
            return NPT.localize(dt)
        except ValueError as e:
            logging.error(f"Error parsing date: {e}")
            return None

    def check_if_valid_time(self, published_time):
        now = datetime.now(NPT)
        logging.info(f"Published Time: {published_time}")
        time_diff = (now - published_time).total_seconds() / 3600
        logging.info(f"Time Difference (hours): {time_diff}")
        return time_diff <= VALID_TIME

    def fetch_articles(self, category_url: str, headers: dict):
        """Fetch articles from the given category URL."""
        try:
            response = requests.get(category_url, headers=headers)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                logging.error(
                    f"Failed to fetch articles: {response.status_code} - {response.text}"
                )
        except Exception as e:
            logging.error(f"Error fetching articles: {e}")
        return None

    def extract_articles(self, soup):
        articles = []
        if soup:
            for article in soup.select(".categories-list-info div"):
                link = article.find("a")["href"] if article.find("a") else None
                published_at = (
                    article.select_one(".headline-time").get_text(strip=True)
                    if article.select_one(".headline-time")
                    else None
                )
                if link and published_at:
                    full_link = self.base_url + link
                    articles.append((full_link, published_at))
                    logging.info(
                        f"Extracted article link: {full_link} with published time: {published_at}"
                    )
        return articles

    def scrape_full_article(self, link: str, headers: dict):
        try:
            full_article_response = requests.get(link, headers=headers)
            if full_article_response.status_code == 200:
                return BeautifulSoup(full_article_response.text, "html.parser")
            else:
                logging.error(
                    f"Failed to scrape full article: {full_article_response.status_code} - {full_article_response.text}"
                )
        except Exception as e:
            logging.error(f"Error scraping full article: {e}")
        return None

    def extract_article_details(self, full_soup):
        content = (
            full_soup.select_one(".news-content").get_text(strip=True)
            if full_soup.select_one(".news-content")
            else "No Content"
        )
        image = (
            full_soup.select_one(".inner-featured-image img")["src"]
            if full_soup.select_one(".inner-featured-image img")
            else "No Image"
        )
        main_heading = (
            full_soup.select_one("div.main-heading h2").text.strip()
            if full_soup.select_one(".main-heading")
            else "No Main Heading"
        )
        return main_heading, content, image
