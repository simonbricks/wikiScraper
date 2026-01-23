# unit tests on the functionality of the wiki_argparser.py module

import pytest

from modules.argparser import WikiParser
from assets.arg_classes import Args
from assets.arg_classes import SummaryTableArgs, FreqWordArgs, WordCountArgs
from assets.errors import ArgValidationError


def test_no_functionalities():
    args = Args(
        SummaryTableArgs(),
        FreqWordArgs(),
        WordCountArgs()
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert False
    except ArgValidationError:
        assert True


def test_empty_summary():
    args = Args(
        SummaryTableArgs(summary=""),
        FreqWordArgs(),
        WordCountArgs()
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert False
    except ArgValidationError:
        assert True


def test_incorrect_mode_value():
    args = Args(
        SummaryTableArgs(
            summary="Aawkwaard",
            table="Aawkwaard",
            number=1,
            first_row_is_header=True
        ),
        FreqWordArgs(
            analyze_relative_word_fq=True,
            mode="artikel",  # wrong
            count=5,
            chart="some_filepath"
        ),
        WordCountArgs(
            count_words="Aawkwaard",
            auto_count_words="Aawkwaard",
            depth=5,
            wait=5
        )
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert False
    except ArgValidationError:
        assert True


def test_misssing_codependent_args():
    args = Args(
        SummaryTableArgs(
            table="someArticle",
            first_row_is_header=True
            ),
        FreqWordArgs(),
        WordCountArgs()
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert False
    except ArgValidationError:
        assert True


def test_correct_args1():
    args = Args(
        SummaryTableArgs(
            summary="Aawkwaard",
            table="Aawkwaard",
            number=1,
            first_row_is_header=True
        ),
        FreqWordArgs(),
        WordCountArgs(
            count_words="Aawkwaard",
        )
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert True
    except ArgValidationError:
        assert False


def test_correct_args2():
    args = Args(
        SummaryTableArgs(
            summary="Aawkwaard",
            table="Aawkwaard",
            number=1,
            first_row_is_header=True
        ),
        FreqWordArgs(
            analyze_relative_word_fq=True,
            mode="article",
            count=5,
            chart="some_filepath"
        ),
        WordCountArgs(
            count_words="Aawkwaard",
            auto_count_words="Aawkwaard",
            depth=5,
            wait=5
        )
    )

    parser = WikiParser(args)

    try:
        parser.parse_args()
        assert True
    except ArgValidationError:
        assert False
