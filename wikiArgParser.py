import argparse


class wikiParser():
    parser = argparse.ArgumentParser(
        description='SporeScraper - analiza danych strony spore.fandom.com',
        epilog='Szymon Cegłowski 2026, program zgodny z licencją CC-BY-SA')

    def __init__(self):
        self.parser.add_argument('--summary',
                                 type=str,
                                 help='Fraza na wiki')
        self.parser.add_argument('--table',
                                 type=str,
                                 help='Fraza na wiki')
        self.parser.add_argument('--number',
                                 type=int,
                                 help='Kolejność tabeli na stronie')
        self.parser.add_argument('--first-row-is-header',
                                 action='store_true',
                                 help='Uwzględnienie nagłówków tabeli')
        self.parser.add_argument('--count-words',
                                 type=str,
                                 help='Fraza na wiki')
        self.parser.add_argument('--analyze-relative-word-frequency',
                                 action='store_true',
                                 help='Analiza częstości wyrazów strony')
        self.parser.add_argument('--mode',
                                 type=str,
                                 help='Możliwe wartości: [article, language]')
        self.parser.add_argument('--chart',
                                 type=str,
                                 help='Ścieżka do zapisania pliku')
        self.parser.add_argument('--auto-count-words',
                                 type=str,
                                 help='Początkowa szukana fraza')
        self.parser.add_argument('--depth',
                                 type=int,
                                 help='Maksymalna głębokość strony od podanej')
        self.parser.add_argument('--wait',
                                 type=int,
                                 help='Liczba sekund między --count-words')

    def parse_args(self):
        return self.parser.parse_args()