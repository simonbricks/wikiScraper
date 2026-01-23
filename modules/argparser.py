from assets.arg_classes import Args
from assets.errors import ArgValidationError


class WikiParser():
    def __init__(self, args: Args):
        self.args = args

    
    def _validate_args(self):
        """
        Checks and confirms that the gathered command-line arguments
        were input correctly.
        Throws a parser error otherwise.
        """

        functionalities = [
            self.args.summary,
            self.args.table,
            self.args.analyze_relative_word_fq,
            self.args.count_words,
            self.args.auto_count_words
        ]

        if not any(functionalities):
            raise ArgValidationError("""No functionalities chosen,
                                        use --h for help""")

        arg_table = self.args.table is not None
        arg_number = self.args.number is not None
        arg_header = self.args.first_row_is_header is not None

        if (arg_table and not arg_number) or (arg_number and not arg_table):
            raise ArgValidationError("""--table and --number arguments 
                                        are codependent, use both""")

        if arg_header and not (arg_table):
            raise ArgValidationError("""The --first-row-is-header argument
                                        needs the --table and --number
                                        arguments to be valid""")

        arg_rw = self.args.analyze_relative_word_fq is not None
        arg_mode = self.args.mode is not None
        arg_count = self.args.count is not None
        arg_chart = self.args.chart is not None

        is_empty_rw_argument = any([arg_rw, arg_mode, arg_count])
        is_not_empty_rw_argument = not all([arg_rw, arg_mode, arg_count])

        if is_empty_rw_argument and is_not_empty_rw_argument:
            raise ArgValidationError("""The arguments
                                        --analyze-relative-word-frequency
                                        --mode and --count
                                        are codependent, use all of them""")

        if arg_chart and not arg_rw:
            raise ArgValidationError("""The --chart argument needs the
                                        --analyze-relative-word-frequency,
                                        --mode and --count arguments to
                                        exist and be valid""")

        if not self.args.mode in [None, "article", "language"]:
            raise ArgValidationError("""The --mode argument's value
                                        is incorrect.
                                        Make sure it's either 'article'
                                        or 'language'.""")

        arg_acw = self.args.auto_count_words
        arg_depth = self.args.depth
        arg_wait = self.args.wait

        is_empty_acw_argument = any([arg_acw, arg_depth, arg_wait])
        is_not_empty_acw_argument = not all([arg_acw, arg_depth, arg_wait])

        if is_empty_acw_argument and is_not_empty_acw_argument:
            raise ArgValidationError("""The arguments --auto-count-words,
                                        --depth and --wait are codependent,
                                        use all of them""")


    def parse_args(self):
        """Parses and returns the command-line arguments to other modules."""
        self._validate_args()
        return self.args
