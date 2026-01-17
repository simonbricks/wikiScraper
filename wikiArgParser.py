import argparse


class wikiParser():
    parser = argparse.ArgumentParser(
        description='SporeScraper - tool for spore.fandom wiki data analysis',
        epilog='Szymon Cegłowski 2026, made using the CC-BY-SA licence')

    def __init__(self):
        self.parser.add_argument('--summary',
                                 type=str,
                                 metavar='SEARCH PHRASE',
                                 help='summarize a wiki page')
        self.parser.add_argument('--table',
                                 type=str,
                                 metavar='SEARCH PHRASE',
                                 help='fetch a table from the phrase page')
        self.parser.add_argument('--number',
                                 type=int,
                                 help='the order of the table on the page')
        self.parser.add_argument('--first-row-is-header',
                                 action='store_true',
                                 help='input the table including its headers')
        self.parser.add_argument('--count-words',
                                 type=str,
                                 metavar='SEARCH PHRASE',
                                 help='''create a JSON file with the frequency
                                         of page word counts''')
        self.parser.add_argument('--analyze-relative-word-frequency',
                                 action='store_true',
                                 help='analyze the word frequency on the page')
        self.parser.add_argument('--mode',
                                 type=str,
                                 metavar='[\'article\', \'language\']',
                                 help='''reference point of the analysis''')
        self.parser.add_argument('--chart',
                                 type=str,
                                 metavar='FILEPATH',
                                 help='make and save a word frequency chart')
        self.parser.add_argument('--auto-count-words',
                                 type=str,
                                 metavar='STARTING SEARCH PHRASE',
                                 help='run --count-words on multiple pages')
        self.parser.add_argument('--depth',
                                 type=int,
                                 help='''max depth of analyzed pages
                                         from the starting one''')
        self.parser.add_argument('--wait',
                                 type=int,
                                 help='seconds to wait between --count-words')

    def parse_args(self):
        return self.parser.parse_args()
