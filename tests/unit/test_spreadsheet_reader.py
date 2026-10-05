import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from acoustic_report.adapters.spreadsheet_reader import read_workbook
from acoustic_report.domain.models import InputValidationError


class SpreadsheetReaderTest(unittest.TestCase):
    def test_missing_sheets_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "invalid.xlsx"
            Workbook().save(path)
            with self.assertRaisesRegex(InputValidationError, "Fehlende Tabellenblätter"):
                read_workbook(path)


if __name__ == "__main__":
    unittest.main()
