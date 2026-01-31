import argparse
from modules.argparser import WikiParser
from assets.arg_classes import Args
from assets.arg_classes import FreqWordArgs, SummaryTableArgs, WordCountArgs


def collect_cmd_args() -> Args:
    """
    Collects the command line arguments from the run instance of 
    wiki_scraper.py and places then inside a general Args object.
    """
    
    parser = argparse.ArgumentParser(
        description='SporeScraper - tool for spore.fandom wiki data analysis',
        epilog='Szymon Cegłowski 2026, made using the CC-BY-SA licence')

    parser.add_argument('--summary',
                        type=str,
                        metavar='SEARCH PHRASE',
                        help='summarize a wiki page')

    parser.add_argument('--table',
                        type=str,
                        metavar='SEARCH PHRASE',
                        help='fetch a table from the phrase page')

    parser.add_argument('--number',
                        type=int,
                        help='the order of the table on the page')

    parser.add_argument('--first-row-is-header',
                        action='store_true',
                        default=None,  # made to simplify the parsing process
                        help='input the table including its headers')

    parser.add_argument('--count-words',
                        type=str,
                        metavar='SEARCH PHRASE',
                        help='''create a JSON file with the frequency
                                of page word counts''')

    parser.add_argument('--analyze-relative-word-frequency',
                        action='store_true',
                        default=None,
                        help='analyze the word frequency on the page')

    parser.add_argument('--mode',
                        type=str,
                        metavar='[\'article\', \'language\']',
                        help='reference point of the analysis')

    parser.add_argument('--count',
                        type=int,
                        metavar='NUMBER',
                        help='how many words from the wiki will be compared')

    parser.add_argument('--chart',
                        type=str,
                        metavar='FILEPATH',
                        help='make and save a word frequency chart')

    parser.add_argument('--auto-count-words',
                        type=str,
                        metavar='STARTING SEARCH PHRASE',
                        help='run --count-words on multiple pages')

    parser.add_argument('--depth',
                        type=int,
                        metavar='NUMBER',
                        help='''max depth of analyzed pages
                                from the starting one''')

    parser.add_argument('--wait',
                        type=float,
                        metavar='FLOAT',
                        help='seconds to wait between --count-words')

    args = parser.parse_args()

    collected_args = Args(
        summary_table_args=SummaryTableArgs(
            summary=args.summary,
            table=args.table,
            number=args.number,
            first_row_is_header=args.first_row_is_header
        ),
        freq_args=FreqWordArgs(
            analyze_relative_word_fq=args.analyze_relative_word_frequency,
            mode=args.mode,
            count=args.count,
            chart=args.chart
        ),
        count_args=WordCountArgs(
            count_words=args.count_words,
            auto_count_words=args.auto_count_words,
            depth=args.depth,
            wait=args.wait
        )
    )

    # checking the validity of collected arguments
    parser = WikiParser(collected_args)
    parser.parse_args()

    return collected_args
