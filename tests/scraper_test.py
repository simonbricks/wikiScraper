# unit tests on the functionality of the scraper.py module

import pytest
import os

from modules.scraper import Scraper
from assets.errors import ArgValidationError, PageValidationError
from assets.errors import HTMLFileError


SPORE_FANDOM_URL = "https://spore.fandom.com/wiki/" 


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


def test_too_many_files():
    file1 = open("awwkward1.html", "w")
    file2 = open("creature_stage2.html", "w")

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

    os.remove("awwkward1.html")
    os.remove("creature_stage2.html")


def test_empty_file():
    file = open("awwkward1.html", "x")

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
    
    os.remove("awwkward1.html")


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
        soup = scraper.scrape()
    except Exception:
        assert False
    
    if soup.text:
        assert True
    else:
        assert False
