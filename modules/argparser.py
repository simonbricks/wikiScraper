from assets.arg_classes import Args
from assets.errors import ArgValidationError

import os


class WikiParser():
    """
    Validates arguments given through the command line or manually.
    """
    
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
            raise ArgValidationError(
                "No functionalities chosen, use --h for help"
            )

        arg_table = self.args.table is not None
        arg_number = self.args.number is not None
        arg_header = self.args.first_row_is_header is not None

        if (arg_table and not arg_number) or (arg_number and not arg_table):
            raise ArgValidationError(
                "--table and --number arguments are codependent, use both"
            )

        if arg_header and not (arg_table):
            raise ArgValidationError(
                "The --first-row-is-header argument requires\n"
                "   --table and\n"
                "   --number\n"
                "arguments to be valid"
            )

        arg_rw = self.args.analyze_relative_word_fq is not None
        arg_mode = self.args.mode is not None
        arg_count = self.args.count is not None
        arg_chart = self.args.chart is not None

        is_empty_rw_argument = any([arg_rw, arg_mode, arg_count])
        is_not_empty_rw_argument = not all([arg_rw, arg_mode, arg_count])

        if is_empty_rw_argument and is_not_empty_rw_argument:
            raise ArgValidationError(
                "The arguments:\n"
                "   --analyze-relative-word-frequency\n"
                "   --mode\n"
                "   --count\n"
                "are codependent, use all of them"
            )

        if arg_chart and not arg_rw:
            raise ArgValidationError(
                "The --chart argument requiers the:\n"
                "   --analyze-relative-word-frequency\n"
                "   --mode\n"
                "   --count\n"
                "arguments to be valid"
            )

        if self.args.mode not in [None, "article", "language"]:
            raise ArgValidationError(
                "The --mode argument's value is incorrect.\n"
                "Make sure it's either 'article' or 'language'."
            )

        if self.args.chart:
            chart_path = self.args.chart

            # for the os library to read the path correctly
            if chart_path[0] != "/":
                chart_path = "/" + chart_path

            chart_dir_path = os.path.split(chart_path)[0]

            if not os.path.exists(chart_dir_path):
                raise ArgValidationError(
                    "The --chart argument's value is incorrect.\n"
                    "Make sure it points to an existing directory."
                )

        arg_acw = self.args.auto_count_words
        arg_depth = self.args.depth
        arg_wait = self.args.wait

        is_empty_acw_argument = any([arg_acw, arg_depth, arg_wait])
        is_not_empty_acw_argument = not all([arg_acw, arg_depth, arg_wait])

        if is_empty_acw_argument and is_not_empty_acw_argument:
            raise ArgValidationError(
                "The arguments:\n"
                "   --auto-count-words\n"
                "   --depth\n"
                "   --wait\n"
                "are codependent, use all of them"
            )


    def parse_args(self):
        """Parses and returns the command-line arguments to other modules."""
        self._validate_args()
        return self.args
