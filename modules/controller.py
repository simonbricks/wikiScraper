from assets.arg_classes import Args
from bs4 import BeautifulSoup, NavigableString, Tag

from modules.scraper import Scraper

import csv
import json
import time  # for time.sleep()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # for bar graph plotting

from wordfreq import top_n_list, word_frequency


# how many of the most common words in the wiki's language to analyze
NUM_MOST_COMMON_LANG_WORDS = 1000
WIKI_LANG = "en"
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


    def _get_page_contents(self, wiki_url: str, search_phrase: str,
                           use_local_html_file: bool = False):
        """
        Returns a BeautifulSoup of the
        article contents of the searched wiki page.
        """

        scraper = Scraper(
            wiki_url=wiki_url,
            search_phrase=search_phrase,
            use_local_html_file_instead=use_local_html_file
        )
        page_html = scraper.scrape()

        soup = BeautifulSoup(page_html, "html.parser")
        content = soup.find("div", attrs={"class": "mw-content-ltr"})
        cleaned_content = self._clean_up_soup(content)

        return cleaned_content


    def summarize(self, use_local_html_file: bool = False):
        """
        Module responsible for the --summary functionality,
        downloads the wiki page source code and returns its summary.
        """
        if use_local_html_file:  # for the integration test
            soup = self._get_page_contents(
                wiki_url=SPORE_FANDOM_URL,
                search_phrase="test phrase",
                use_local_html_file=use_local_html_file
            )
        else:  # if used through the controller run() function
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

        cols = []

        for table_header in examined_table.find_all("th"):
            # collecting all header items
            cols.append(table_header.text.strip())

        for t_row in examined_table.find_all("tr")[1:]:
            # collecting all other table items
            table_row = []
            # the first tr is the header, so we skip it
            columns = t_row.find_all("td")

            if (columns):
                for item in columns:
                    table_row.append(item.text.strip())
                table_contents.append(table_row)
        
        # creating a pandas DataFrame so that the table looks better
        df = pd.DataFrame(
            np.array(table_contents),
            columns=cols
        )

        print(df)

        # setting up the first column of the table as an index
        df.set_index(df.columns[0], inplace=True)
        
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
                search_phrase=page_url,
            )
        else:
            soup = self._get_page_contents(
                wiki_url=SPORE_FANDOM_URL,
                search_phrase=self.args.count_words,
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


    def _create_bar_chart(self, df: pd.DataFrame):
        """
        Creates a bar chart based on the collected word frequency
        comparison table and saves it in the file path given by the
        --chart argument.
        """

        categories = df["Word"]
        article_group = df["Frequency in article"]
        wiki_group = df["Frequency in wiki language"]

        bar_width = 0.35

        r_article = np.arange(len(article_group))
        r_wiki = [x + bar_width for x in r_article]

        plt.bar(
            r_article,
            article_group,
            color="red",
            width=bar_width,
            label="Frequency in wiki articles"
        )

        plt.bar(
            r_wiki,
            wiki_group,
            color="blue",
            width=bar_width,
            label="Frequency in wiki language"
        )

        plt.xlabel("Words compared", fontweight="bold")
        plt.xticks(
            [r + 0.5*bar_width for r in range(len(article_group))],
            categories,
            rotation=45
        )

        plt.ylabel("Frequency", fontweight="bold")
        plt.title("Frequency comparison for words")
        plt.legend()

        plt.savefig(self.args.chart, bbox_inches="tight")


    def analyze_relative_word_fq(self):
        """
        Performs an analysis of the frequency of the words used in the
        wiki articles collected by the --count-words argument over multiple
        code runs and if the --chart argument was given visualizes the
        findings using a bar chart.
        """

        # collecting the most common words in the wiki language
        top_lang_words = top_n_list(WIKI_LANG, NUM_MOST_COMMON_LANG_WORDS)

        # collecting the list of the frequency of the words on the wiki
        try:
            f = open("word-counts.json", "r")
            file_contents = f.read()

            if file_contents:
                wiki_words = json.loads(file_contents)
        except FileNotFoundError:
            f = open("word-counts.json", "w")

            print("""File word-counts.json does not exist, 
                     so the word frequency analysis can't be performed""")
            return  # the lack of a file shouldn't result in an error
        
        sum_of_word_count = sum(wiki_words.values())

        most_common_lang_word_fq = word_frequency(
            top_lang_words[0],
            WIKI_LANG
        )

        # the number of rows of the comparison table
        rows_no = self.args.count

        # list of blocks of values to collect for the comparison table
        comparison_list = []
        comparison_headers = [
            "Word",
            "Frequency in article",
            "Frequency in wiki language"
        ]

        if self.args.mode == "article":
            # turning the wiki word count dictionary to a list
            wiki_words_list = list(wiki_words.items())

            # sorting the list by the number of apperances
            wiki_words_list_sorted = sorted(
                wiki_words_list,
                key=lambda tup: tup[1],
                reverse=True  # to maintain descending order
            )

            n_most_common_wiki_words = wiki_words_list_sorted[:rows_no]

            for item in n_most_common_wiki_words:
                word = item[0]

                if not word in top_lang_words:
                    comparison_list.append(
                        [
                            word,
                            wiki_words[word] / sum_of_word_count,
                            np.nan
                        ]
                    )
                else:
                    lang_word_fq = word_frequency(word, WIKI_LANG)
                    comparison_list.append(
                        [
                            word,
                            wiki_words[word] / sum_of_word_count,
                            word_frequency(word, WIKI_LANG)
                        ]
                    )
            comparison_list = np.array(comparison_list)

        else:  # self.args.mode == "language"
            n_most_common_lang_words = top_lang_words[:rows_no]

            for word in n_most_common_lang_words:
                # the word is in the collected wiki words
                if not word in wiki_words.keys():
                    comparison_list.append(
                        [
                            word,
                            np.nan,
                            word_frequency(word, WIKI_LANG)
                        ]
                    )
                else:
                    comparison_list.append(
                        [
                            word,
                            wiki_words[word] / sum_of_word_count,
                            word_frequency(word, WIKI_LANG)
                        ]
                    )
        
        # creating a comparison DataFrame with pandas
        df = pd.DataFrame(
            comparison_list,
            columns=comparison_headers
        )

        df["Frequency in article"] = pd.to_numeric(
            df["Frequency in article"],
            errors="coerce"
        )

        df["Frequency in wiki language"] = pd.to_numeric(
            df["Frequency in wiki language"],
            errors="coerce"
        )
        
        print(df)
        # creating a file with a bar chart in the root directory
        if self.args.chart:
            self._create_bar_chart(df)


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
