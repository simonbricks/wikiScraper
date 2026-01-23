import pytest

from modules.controller import Controller
from assets.arg_classes import Args
from assets.arg_classes import SummaryTableArgs, WordCountArgs, FreqWordArgs


def test_summary_module():
    args = Args(
        SummaryTableArgs(summary="Cell_Stage")
    )
    controller = Controller(args)

    content = controller.summarize()
    if content:
        assert True
    else:
        assert False

