import unittest

from acoustic_report.domain.acoustic_rules import assess_receivers, energetic_sum
from acoustic_report.domain.models import (
    AcousticDataset,
    Contribution,
    InputValidationError,
    NoiseSource,
    Receiver,
)


class AcousticRulesTest(unittest.TestCase):
    def test_equal_levels_gain_three_db(self):
        self.assertAlmostEqual(energetic_sum([50.0, 50.0]), 53.0103, places=3)

    def test_receiver_is_assessed_against_limit(self):
        dataset = AcousticDataset(
            sources=(NoiseSource("S1", "Synthetic source", 90.0),),
            receivers=(Receiver("R1", "Synthetic receiver", "Mixed use", 60.0),),
            contributions=(Contribution("R1", "S1", 54.5),),
        )
        result = assess_receivers(dataset)[0]
        self.assertEqual(result.rating_level_db, 55)
        self.assertEqual(result.margin_db, 5)
        self.assertTrue(result.compliant)

    def test_missing_contribution_is_rejected(self):
        dataset = AcousticDataset(
            sources=(NoiseSource("S1", "Synthetic source", 90.0),),
            receivers=(Receiver("R1", "Synthetic receiver", "Mixed use", 60.0),),
            contributions=(),
        )
        with self.assertRaisesRegex(InputValidationError, "fehlen Pegelbeiträge"):
            assess_receivers(dataset)


if __name__ == "__main__":
    unittest.main()
