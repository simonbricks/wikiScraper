from assets.arg_classes import Args
from bs4 import BeautifulSoup, NavigableString, Tag

from modules.scraper import Scraper

import csv
import json
import time  # for using time.sleep() only


SPORE_FANDOM_URL = "https://spore.fandom.com/" 


class Controller:
    """
    Takes arguments from wiki_scraper.py validated by argparser module
    and realizes the project functionalities in accordance with them.
    """

    def __init__(self, args : Args):
        self.args = args


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


    def _clean_up_word(self, word: str) -> str:
        """
        Removes characters that are not letters or numbers
        from the word.
        """

        if word.isalnum():
            return word
        
        else:
            chars_to_delete = []

            for char in word:
                if not char.isalnum() and not char in chars_to_delete:
                    chars_to_delete.append(char)
            
            for char in chars_to_delete:
                word = word.replace(char, "")
            return word


    def _get_page_contents(self, wiki_url: str, search_phrase: str):
        """
        Returns a BeautifulSoup of the
        article contents of the searched wiki page.
        """

        scraper = Scraper(
            wiki_url=wiki_url,
            search_phrase=search_phrase
        )
        page_html = scraper.scrape()

        soup = BeautifulSoup(page_html, "html.parser")
        content = soup.find("div", attrs={"class": "mw-content-ltr"})
        cleaned_content = self._clean_up_soup(content)

        return cleaned_content


    def summarize(self):
        """
        Module responsible for the --summary functionality,
        downloads the wiki page source code and returns its summary.
        """

        soup = self._get_page_contents(
            wiki_url=SPORE_FANDOM_URL,
            search_phrase=self.args.summary
        )

        first_p = soup.find("p")
        summary_text = first_p.text.strip('\n')  # unnecessary indents

        print(summary_text)
        return summary_text  # for testing


    def save_table(self):
        """
        Module responsible for executing the --table functionality,
        downloads the wiki page source code, prints out the data from
        the indicated table (in the run() function)
        and saves it to a .csv file titled by the
        search phrase.
        """

        soup = self._get_page_contents(
            wiki_url=SPORE_FANDOM_URL,
            search_phrase=self.args.table
        )

        # picking up all the tables concerning the wikipage content
        all_tables = soup.find_all("table", attrs={"class": "wikitable"})

        # we add one here, because the indexing starts from 0
        examined_table = all_tables[self.args.number - 1]
        
        table_contents = []

        # printing out the table so that it's readable

        header_row = []
        for table_header in examined_table.find_all("th"):
            # collecting all header items
            header_row.append(table_header.text.strip())
            print(table_header.text.strip(), end=" | ")

        table_contents.append(header_row)

        print()

        for t_row in examined_table.find_all("tr")[1:]:
            # collecting all other table items
            table_row = []
            # the first tr is the header, so we skip it
            columns = t_row.find_all("td")

            if (columns):
                for item in columns:
                    table_row.append(item.text.strip())
                    print(item.text.strip(), end=" | ")
                table_contents.append(table_row)
                print()
        
        # writing the table contents to a .csv file
        with open(f"{self.args.table}.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(table_contents)


    def count_words(self, page_url: str = None):
        """
        Counts words in a given wiki article,
        and keeps track of their count over many runs
        in a JSON file.

        page_url is an optional argument used in auto_count_words() function.
        """

        if page_url:  # used in the auto_count_words() function
            soup = self._get_page_contents(
                wiki_url=SPORE_FANDOM_URL,
                search_phrase=page_url
            )
        else:
            soup = self._get_page_contents(
                wiki_url=SPORE_FANDOM_URL,
                search_phrase=self.args.count_words
            )

        # counting words and saving them to the .json file
        word_count = {}

        try:
            f = open("word-counts.json", "r")
            file_contents = f.read()

            if file_contents:
                word_count = json.loads(file_contents)
        except FileNotFoundError:
            f = open("word-counts.json", "w")  # creating an empty file

        if word_count:
            word_count["times_ran"] += 1
        else:
            word_count = {
                "times_ran": 1
            }
        
        list_of_words = soup.text.split()

        for word in list_of_words:
            word = self._clean_up_word(word)  # removes ',' and other symbols

            if word.lower() in word_count:
                word_count[word.lower()] += 1
            else:
                word_count[word.lower()] = 1
        
        word_count_json = json.dumps(word_count)
        
        with open("word-counts.json", "w") as f:
            f.write(word_count_json)


    def analyze_relative_word_fq(self):
        pass


    def auto_count_words(self):
        """
        Runs --count-words on all pages that have page depth
        lower or equal to --depth argument from the requested
        search phrase wikipage.
        """

        visited_pages = []
        visited_pages.append(
            [self.args.auto_count_words, 0]
        )

        for page_dfs in visited_pages:
            if page_dfs[1] > self.args.depth:
                break
            
            soup = self._get_page_contents(
                wiki_url=SPORE_FANDOM_URL,
                search_phrase=page_dfs[0]
            )
            self.count_words(page_dfs[0])

            all_links = soup.find_all("a")

            for link in all_links:
                # looking for only the wiki article pages
                if link["href"][:5] == "/wiki":
                    visited_pages.append(
                        [link["href"], page_dfs[1] + 1]
                    )
            time.sleep(self.args.wait)


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
