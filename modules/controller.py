from assets.arg_classes import Args
from bs4 import BeautifulSoup

from modules.scraper import Scraper


SPORE_FANDOM_URL = "https://spore.fandom.com/wiki/" 


class Controller:
    """
    Takes arguments from wiki_scraper.py validated by argparser module
    and realizes the project functionalities in accordance with them.
    """

    def __init__(self, args : Args):
        self.args = args


    def summarize(self):
        pass


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
