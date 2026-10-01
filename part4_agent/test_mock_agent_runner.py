import unittest
import os

from mock_agent_runner import run


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APRIL_FEED = os.path.join(
    BASE_DIR,
    "part2_engine",
    "fixtures",
    "monthly_category_revenue.csv",
)

MAY_FEED = APRIL_FEED
JUNE_FEED = APRIL_FEED

CORRUPTED_FEED = os.path.join(
    BASE_DIR,
    "part2_engine",
    "fixtures",
    "corrupted_feed.csv",
)


class TestMockAgentRunner(unittest.TestCase):

    def test_may_scenario(self):
        result = run(
            "May",
            APRIL_FEED,
            MAY_FEED
        )

        self.assertEqual(result["validation_status"], "valid")

        flagged = result["flagged_categories"]

        self.assertEqual(
            [x["category"] for x in flagged],
            ["Ethnic Wear", "Western Wear", "Kids Wear"]
        )

        self.assertEqual(
            [x["mom_pct"] for x in flagged],
            [77.1, -23.6, -23.48]
        )

        self.assertEqual(
            set(result["suppressed_categories"]),
            {"Beauty & Personal Care", "Home & Kitchen"}
        )

        self.assertEqual(result["escalated_categories"], [])
        self.assertEqual(
            result["action_taken"],
            "drafted_and_held_for_approval"
        )

    def test_june_scenario(self):
        result = run(
            "June",
            MAY_FEED,
            JUNE_FEED
        )

        self.assertEqual(result["validation_status"], "valid")

        flagged = result["flagged_categories"]

        self.assertEqual(
            [x["category"] for x in flagged],
            ["Ethnic Wear", "Home & Kitchen", "Kids Wear"]
        )

        self.assertEqual(
            [x["mom_pct"] for x in flagged],
            [-58.74, 42.59, 23.9]
        )

        self.assertEqual(
            result["suppressed_categories"],
            ["Western Wear"]
        )

        self.assertNotIn(
            "Beauty & Personal Care",
            [x["category"] for x in flagged]
        )

        self.assertNotIn(
            "Beauty & Personal Care",
            result["suppressed_categories"]
        )

        self.assertEqual(result["escalated_categories"], [])

    def test_corrupted_feed_hard_stop(self):
        result = run(
            "July",
            MAY_FEED,
            CORRUPTED_FEED
        )

        self.assertEqual(result["run_month"], "July")
        self.assertEqual(result["validation_status"], "invalid")

        self.assertEqual(
            result["validation_errors"],
            [
                "line 3: negative revenue (-4200.0) for category=Western Wear",
                "line 4: missing category (month=July)",
                "line 6: missing revenue (category=Home & Kitchen)",
            ]
        )

        self.assertEqual(result["flagged_categories"], [])
        self.assertEqual(result["suppressed_categories"], [])
        self.assertEqual(result["escalated_categories"], [])
        self.assertEqual(result["action_taken"], "hard_stop")


if __name__ == "__main__":
    unittest.main()
