from assets.arg_classes import Args
from bs4 import BeautifulSoup, NavigableString, Tag

from modules.scraper import Scraper


SPORE_FANDOM_URL = "https://spore.fandom.com/wiki/" 


class Controller:
    """
    Takes arguments from wiki_scraper.py validated by argparser module
    and realizes the project functionalities in accordance with them.
    """

    def __init__(self, args : Args):
        self.args = args


    def _get_page_contents(self, wiki_url: str, search_phrase: str):
        """
        Returns a BeautifulSoup of the contents of the searched wiki page.
        """

        scraper = Scraper(wiki_url, search_phrase)
        page_html = scraper.scrape()

        soup = BeautifulSoup(page_html, "html.parser")
        content = soup.find("div", attrs={"class": "mw-content-ltr"})

        return content


    def summarize(self):
        """
        Module responsible for the --summary functionality,
        downloads the wiki page source code and prints out its summary.
        """

        content = self._get_page_contents(
            wiki_url=SPORE_FANDOM_URL,
            search_phrase=self.args.summary
        )
        
        # getting rid of the infobox that is inside the <p> tag
        infobox = content.find("aside", attrs={"class": "portable-infobox"})
        infobox.extract()

        first_p = content.find("p")
        summary_text = first_p.text.strip('\n')  # unnecessary indents

        return summary_text


    def save_table(self):
        pass


    def count_words(self):
        pass


    def analyze_relative_word_fq(self):
        pass


    def auto_count_words(self):
        pass


    def run(self):
        """
        Manages project functionalities and modules
        according to given arguments.
        """

        if self.args.summary:
            self.summarize()

        if self.args.table:
            self.save_table()
        
        if self.args.count_words:
            self.count_words()

        if self.args.analyze_relative_word_fq:
            self.analyze_relative_word_fq()

        if self.args.auto_count_words:
            self.auto_count_words()
