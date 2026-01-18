# a file containing smaller structures that make the code more readable

class SummaryTableArgs():
    def __init__(self, summary: str = None, table: str = None,
                 number: int = None, first_row_is_header: bool = False):
        self.summary = summary
        self.table = table
        self.number = number
        self.first_row_is_header = first_row_is_header


class FreqWordArgs():
    def __init__(self, analyze_relative_word_frequency: bool = False,
                 mode: str = None, count: int = None, chart: str = None):
        self.analyze_relative_word_fq = analyze_relative_word_frequency
        self.mode = mode
        self.count = count
        self.chart = chart


class CountAndAutoArgs():
    def __init__(self, count_words: str = None, auto_count_words: str = None,
                 depth: int = None, wait: int = None):
        self.count_words = count_words
        self.auto_count_words = auto_count_words
        self.depth = depth
        self.wait = wait

# holds the arguments that are to be passed down to the argparser
class Args():
    def __init__(self,
                 summary_args: SummaryTableArgs = None,
                 freq_args: FreqWordArgs = None,
                 count_args: CountAndAutoArgs = None):
        self.summary_args = summary_args
        self.freq_args = freq_args
        self.count_args = count_args
