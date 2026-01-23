# a file containing smaller structures that make the code more readable


""" 
A class of arguments for the WikiParser concerning the 
--summary and --table functionality.
"""
class SummaryTableArgs():
    def __init__(self, summary: str = None, table: str = None,
                 number: int = None, first_row_is_header: bool = None):
        self.summary = summary
        self.table = table
        self.number = number
        self.first_row_is_header = first_row_is_header


""" 
A class of arguments for the WikiParser concerning the 
--analyze-relative-word-frequency functionality.
"""
class FreqWordArgs():
    def __init__(self, analyze_relative_word_fq: bool = None,
                 mode: str = None, count: int = None, chart: str = None):
        self.analyze_relative_word_fq = analyze_relative_word_fq
        self.mode = mode
        self.count = count
        self.chart = chart


""" 
A class of arguments for the WikiParser concerning the 
--count-words and --auto-count-words functionality.
"""
class WordCountArgs():
    def __init__(self, count_words: str = None, auto_count_words: str = None,
                 depth: int = None, wait: int = None):
        self.count_words = count_words
        self.auto_count_words = auto_count_words
        self.depth = depth
        self.wait = wait


""" 
A class of all collected arguments for the WikiParser. 
"""
# holds the arguments that are to be passed down to the argparser
class Args():
    def __init__(self,
                 summary_table_args: SummaryTableArgs = None,
                 freq_args: FreqWordArgs = None,
                 count_args: WordCountArgs = None):
        # unpacking the collected arguments
        if summary_table_args:
            self.summary = summary_table_args.summary
            self.table = summary_table_args.table
            self.number = summary_table_args.number
            self.first_row_is_header = summary_table_args.first_row_is_header

        if count_args:
            self.count_words = count_args.count_words

            self.auto_count_words = count_args.auto_count_words
            self.depth = count_args.depth
            self.wait = count_args.wait

        if freq_args:
            self.analyze_relative_word_fq = freq_args.analyze_relative_word_fq
            self.mode = freq_args.mode
            self.count = freq_args.count
            self.chart = freq_args.chart
