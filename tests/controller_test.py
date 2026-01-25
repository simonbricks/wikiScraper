import pytest

from modules.controller import Controller
from assets.arg_classes import Args
from assets.arg_classes import SummaryTableArgs, WordCountArgs, FreqWordArgs


def test_word_cleanup():
    word1 = "hello."
    word2 = "you're?"
    word3 = "eyes... ."

    args = Args(
        SummaryTableArgs(summary="Cell_Stage")
    )
    
    controller = Controller(args)

    word1_cleaned = controller._clean_up_word(word1)
    word2_cleaned = controller._clean_up_word(word2)
    word3_cleaned = controller._clean_up_word(word3)

    if word1_cleaned != "hello":
        assert False
    if word2_cleaned != "youre":
        assert False
    if word3_cleaned != "eyes":
        assert False
    assert True


def test_summary_module():
    args = Args(
        SummaryTableArgs(summary="Creature_Stage")
    )
    controller = Controller(args)

    content = controller.summarize()

    creature_stage_summary = "The Creature Stage is the second stage in Spore."
    
    if creature_stage_summary in content:
        assert True
    else:
        assert False

