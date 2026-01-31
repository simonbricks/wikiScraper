import requests
from bs4 import BeautifulSoup

from pathlib import Path

from assets.errors import PageValidationError, HTMLFileError


class Scraper:
    """
    Collects source code of a wiki search phrase page,
    it can also instead take code from a local html file, if needed.

    Returns a BeautifulSoup object of the page html contents.
    """

    def __init__(self, wiki_url: str, search_phrase: str,
                 use_local_html_file_instead: bool = False):
        self.wiki_url = wiki_url
        self.search_phrase = search_phrase
        self.use_local_html = use_local_html_file_instead


    def _clean_up_soup(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Removes unnecessary content from the wiki page soup.
        """
        
        cleaned_soup = soup

        # getting rid of the infobox
        infobox = soup.find("aside", attrs={"class": "portable-infobox"})

        if infobox:
            infobox.extract()

        # getting rid of the table of contents
        toc = soup.find("div", attrs={"id": "toc"})

        if toc:
            toc.extract()

        # getting rid of the navbox at the bottom of the page 
        # and everything after
        navbox = soup.find("table", attrs={"class": "va-navbox-border"})

        if navbox:
            after_navbox = navbox.find_all_next()
        else:
            after_navbox = None

        if after_navbox:
            for item_tag in after_navbox:
                item_tag.extract()

        if navbox:
            navbox.extract()

        return cleaned_soup


    def scrape(self) -> str:
        """
        Scrapes wiki page's source code
        and passes the html code onto the controller module.

        Assumption: 
            - If an HTML file exists,
              it's in the root directory of the project.
            - There should be only one HTML file in the rootdir.
        """

        if self.use_local_html:  # taking the source code from a local file
            root_dir = Path.cwd()
            html_files = list(root_dir.glob(f"{self.search_phrase}.html"))

            if not html_files:
                raise HTMLFileError(
                    "No HTML file of the search_phrase filename found\n"
                    "in the root directory of the project."
                )

            if len(html_files) > 1:
                raise HTMLFileError(
                    "There are too many HTML files in the root directory."
                )

            page_text = html_files[0].read_text(encoding="utf-8")

            if not page_text.strip():  # HTML file is empty
                raise HTMLFileError(
                    "The HTML file with page contents is empty."
                )

            soup = BeautifulSoup(page_text, "html.parser")

        else:  # taking the source code straight from the wiki page
            wiki_search_page = self.wiki_url + self.search_phrase

            scraped_page = requests.get(wiki_search_page)

            page_text = scraped_page.text
            soup = BeautifulSoup(page_text, "html.parser")

            # there isn't a wiki page for this search phrase
            if soup.find("div", attrs={"class": "noarticletext"}):
                raise PageValidationError(
                    "The wiki page for the search phrase:\n"
                    f"{self.search_phrase}\n"
                    "doesn't exist."
                )    
    
        return page_text


    def get_page_contents(self):
        """
        Returns a BeautifulSoup of the
        article contents of the searched wiki page.
        """
        page_html = self.scrape()

        soup = BeautifulSoup(page_html, "html.parser")
        content = soup.find("div", attrs={"class": "mw-content-ltr"})
        cleaned_content = self._clean_up_soup(content)

        return cleaned_content
