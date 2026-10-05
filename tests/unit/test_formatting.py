import unittest

from acoustic_report.domain.formatting import format_db, round_half_up


class FormattingTest(unittest.TestCase):
    def test_half_values_are_rounded_up(self):
        self.assertEqual(round_half_up(54.5), 55)

    def test_db_uses_decimal_comma(self):
        self.assertEqual(format_db(49.25), "49,2 dB(A)")


if __name__ == "__main__":
    unittest.main()
