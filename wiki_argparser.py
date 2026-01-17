import argparse


class WikiParser():
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

    """
    Checks and confirms that the command-line arguments
    were input correctly.
    Throws a parser error otherwise.
    """
    def _validate_arguments(self, args):
        functionalities = [
            args.summary,
            args.table,
            args.count_words,
            args.auto_count_words
        ]

        if not functionalities:
            self.parser.error('No functionalities chosen, use --h for help')

        arg_table = args.table is not None
        arg_number = args.number is not None
        arg_header = args.first_row_is_header is not None

        if (arg_table and not arg_number) or (arg_number and not arg_table):
            self.parser.error("""--table and --number arguments are
                                 codependent, use both of them""")

        if arg_header and not (arg_table):
            self.parser.error("""The --first-row-is-header argument
                                 needs the --table and --number
                                 arguments to exist and be valid""")

        arg_rw = args.analyze_relative_word_frequency is not None
        arg_mode = args.mode is not None
        arg_count = args.count is not None
        arg_chart = args.chart is not None

        required_rw_args = [
            arg_rw,
            arg_mode,
            arg_count,
        ]

        is_empty_rw_argument = any(None in required_rw_args)
        is_not_empty_rw_argument = not all(None in required_rw_args)

        if is_empty_rw_argument and is_not_empty_rw_argument:
            self.parser.error("""The arguments
                                 --analyze-relative-word-frequency
                                 --mode and --count
                                 are codepenedent, use all of them""")

        if arg_chart and not arg_rw:
            self.parser.error("""The --chart argument needs the
                                 --analyze-relative-word-frequency,
                                 --mode and --count arguments to
                                 exist and be valid""")

        arg_acw = args.auto_count_words
        arg_depth = args.depth
        arg_wait = args.wait

        required_acw_args = [
            arg_acw,
            arg_depth,
            arg_wait
        ]

        is_empty_acw_argument = any(None in required_acw_args)
        is_not_empty_acw_argument = not all(None in required_acw_args)

        if is_empty_acw_argument and is_not_empty_acw_argument:
            self.parser.error("""The arguments --auto-count-words, --depth and
                                 --wait are codependent, use all of them""")

    """
    Parses and returns the command-line arguments
    to other modules.
    """
    def parse_args(self):
        args = self.parser.parse_args()
        self.validate_arguments(args)
        return args
