from modules.controller import Controller
from assets.arg_classes import SummaryTableArgs, Args

import os


"""
An integration test for the --summary module that reads from the
'cell_stage_page.html' file contained in the 'tests' package
"""
def main():
    # getting contents from the test wiki page .html file
    with open("tests/cell_stage_page.html", "r") as f:
        html = f.read()
    
    # saving the contents to a temporary file in rootdir
    with open("cell_stage_test.html", "w") as f:
        f.write(html)

    args = Args(
        SummaryTableArgs(summary="cell_stage_test")
    )
    controller = Controller(args)

    summary = controller.summarize(use_local_html_file=True)
    print(f"The summary of the Cell Stage article is: \n{summary}\n")
    os.remove("cell_stage_test.html")

    assert summary.startswith("The Cell Stage")
    assert summary.endswith("through a primordial ooze.")

    print("Integration test passed correctly.")


if __name__ == "__main__":
    main()