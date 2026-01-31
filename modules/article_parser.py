from modules.scraper import Scraper

from bs4 import BeautifulSoup


class Article:
    """
    Processes article contents given by the scraper.
    """

    def __init__(self, wiki_url: str, search_phrase: str,
                 use_local_html_file_instead: bool = False):
        self.scraper = Scraper(
            wiki_url=wiki_url,
            search_phrase=search_phrase,
            use_local_html_file_instead=use_local_html_file_instead
        )
        self.soup = self.scraper.get_page_contents()


    def get_summary(self):
        """
        Returns the summary of the article.
        """

        first_p = None

        for p in self.soup.find_all("p", recursive=False):
            if p.get_text(strip=True):
                first_p = p
                break
        summary_text = first_p.text.strip('\n')  # unnecessary indents
        return summary_text


    def get_table(self, n: int):
        """
        Returns the n-th table in the article.
        """

        # picking up all the tables concerning the wikipage content
        all_tables = self.soup.find_all("table", attrs={"class": "wikitable"})

        # we add one here, because the indexing starts from 0
        examined_table = all_tables[n - 1]
        
        table_contents = []

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

        return table_contents, cols
    

    def get_wordlist(self):
        """
        Returns a list of words in the article.
        """

        return self.soup.text.split()

    
    def get_links(self):
        """
        Returns a list of the links in the article.
        """

        return self.soup.find_all("a")