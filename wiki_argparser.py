from wiki_classes import Args


class WikiParser():
    def __init__(self, args: Args):
        self.args = args

    """
    Checks and confirms that the command-line arguments
    were input correctly.
    Throws a parser error otherwise.
    """
    def _validate_arguments(self):
        functionalities = [
            args.summary_args,
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
        self.validate_arguments()
        return args
