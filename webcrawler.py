import requests

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from urllib import parse
from urllib.parse import urlparse

from base import Base
from website import Website
from page import Page


class Crawler():
    def __init__(self, domain):
        self.domain = domain
        self.scanned_list = []

    def scan_page(self, url, session):
        print(url)
        self.scanned_list.append(url)
        request = requests.get(url)
        request.encoding = 'utf-8'
        html = request.text
        soup = BeautifulSoup(html)

        try:
            self.save_soup(session, soup, url)
        except Exception as e:
            print(e)

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            next_page = self.href_to_url(url, href)
            if not self.is_outgoing(next_page) and next_page not in self.scanned_list:
                if self.is_valid(next_page):
                    self.scan_page(next_page, session)

    def scan_website(self, session):
        url = "http://" + self.domain
        self.scan_page(url, session)

    def href_to_url(self, url, href):
        return parse.urljoin(url, href)

    def is_outgoing(self, url):
        url = urlparse(url)
        if self.domain == url.netloc:
            return False
        if url.netloc[:4] == "www." and self.domain in url.netloc:
            return False
        return True

    def is_valid(self, url):
        if "#" in url:
            return False
        if ".pdf" in url:
            return False
        if ".jpg" in url or ".gif" in url:
            return False
        return True

    def save_soup(self, session, soup, page_url):
        try:
            soup_description = soup.find(
                attrs={"property": "og:description"}).get("content")
        except Exception:
            soup_description = ""

        session.add(Page(title=soup.title.string,
                         description=soup_description,
                         url=page_url,
                         website_id=self.domain))
        session.commit()

    def save_website(self, session):
        session.add(Website(url=self.domain,
                            html=True))


def main():
    engine = create_engine("sqlite:///searchengine.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    crawler = Crawler("24chasa.bg")
    crawler.save_website(session)
    crawler.scan_website(session)

if __name__ == '__main__':
    main()
