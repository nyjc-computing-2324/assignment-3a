from importlib import reload
import subprocess
import sys
import unittest

import main


# limit number of retries
MAX_RETRIES = 5
retries = 0


def fetch_autograding() -> None:
    subprocess.run(["git", "submodule", "update", "--init", "--remote"])
    
def autograding_successfully_imported() -> bool:
    """Check if autograding module is successfully imported.

    If a submodule is imported (e.g. autograding.case), autograding may be imported
    as a namespace module.
    Namespace modules have __file__ attribute set tot None, so we can use that to check
    if autograding was imported as a module and not just a namespace module.
    """
    return (
        "autograding" in locals()
        and locals().get("autograding").__file__
    )

# Force refresh of autograding module from upstream
fetch_autograding()

# autograding submodule might not be successfully fetched on init
# if unsuccessful, we have to fetch it manually
while not autograding_successfully_imported():
    try:
        import autograding
        reload(autograding)
        from autograding.case import FuncCall, InOut, RecursiveCall
    except (ImportError, ModuleNotFoundError):
        fetch_autograding()
        retries += 1
    else:
        break
    if retries >= MAX_RETRIES:
        sys.exit("[import autograding] Too many retries, exiting")


class TestNRIC(autograding.TestInputOutput):
    def setUp(self):
        self.testcases = [
            InOut(input="T0102051F", output="NRIC is valid."),
            InOut(input="S8521097A", output="NRIC is valid."),
            InOut(input="C1234567C", output="NRIC is invalid."),
            InOut(input="S123456B", output="NRIC is invalid."),
        ]


if __name__ == '__main__':
    unittest.main()
