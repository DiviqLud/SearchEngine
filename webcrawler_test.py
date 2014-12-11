import unittest
from webcrawler import Crawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler("hackbulgaria.com")

    def test_is_outgoing(self):
        is_outgoin = self.crawler.is_outgoing("http://hackbulgaria.com/course/")
        self.assertFalse(is_outgoin)

    def test_is_outgoing_with_www(self):
        is_outgoin = self.crawler.is_outgoing("http://www.hackbulgaria.com/course/")
        self.assertFalse(is_outgoin)

    def test_is_outgoing_with_www_with_other_site(self):
        is_outgoin = self.crawler.is_outgoing("http://www.abv.com/course/")
        self.assertTrue(is_outgoin)

if __name__ == '__main__':
    unittest.main()