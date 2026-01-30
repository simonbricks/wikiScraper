# unit tests on the functionality of the scraper.py module

import os

from modules.scraper import Scraper
from assets.errors import PageValidationError
from assets.errors import HTMLFileError


SPORE_FANDOM_URL = "https://spore.fandom.com/wiki/"
USE_ONLINE_TESTS = False


def test_no_file():
    scraper = Scraper(
        wiki_url=SPORE_FANDOM_URL,
        search_phrase="Cell Stage",
        use_local_html_file_instead=True
    )

    try:
        scraper.scrape()
        assert False
    except HTMLFileError:
        assert True


def test_empty_file():
    file = open("awwkward.html", "w")
    file.write(" ")

    scraper = Scraper(
        wiki_url=SPORE_FANDOM_URL,
        search_phrase="awwkward",
        use_local_html_file_instead=True
    )

    try:
        scraper.scrape()
        assert False
    except HTMLFileError:
        assert True

    os.remove("awwkward.html")


def test_valid_file():
    file = open("test_file.html", "w")
    file.write("""
        <h1>This is an HTML file</h1>
        <p>Or at least, it pretends to be so.</p>
        <h6>Actually it would need some more tags like <'head'></h6>
        """)
    file.close()

    scraper = Scraper(
        wiki_url=SPORE_FANDOM_URL,
        search_phrase="test_file",
        use_local_html_file_instead=True
    )

    try:
        html_text = scraper.scrape()
    except Exception:
        assert False

    if html_text:
        assert True
    else:
        assert False

    os.remove("test_file.html")


if USE_ONLINE_TESTS:
    def test_nonexistent_page():
        scraper = Scraper(
            wiki_url=SPORE_FANDOM_URL,
            search_phrase="nonexistent page"
        )

        try:
            scraper.scrape()
            assert False
        except PageValidationError:
            assert True


    def test_valid_page():
        scraper = Scraper(
            wiki_url=SPORE_FANDOM_URL,
            search_phrase="Cell_stage"
        )

        try:
            html_text = scraper.scrape()
        except Exception:
            assert False
        
        if html_text:
            assert True
        else:
            assert False
