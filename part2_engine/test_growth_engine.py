import os
import unittest

from growth_engine import mom_growth, is_flagged, validate_feed


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")


class TestGrowthEngine(unittest.TestCase):

	def test_given_april_may_ethnic_wear_growth_is_flagged(self):
		# GIVEN April -> May Ethnic Wear revenue
		previous = 104520.77
		current = 185107.61

		# WHEN MoM growth is calculated and classified
		growth = mom_growth(previous, current)
		decision = is_flagged(growth)

		# THEN the growth and decision match the specification
		self.assertEqual(growth, 77.1)
		self.assertEqual(decision, "flagged")

	def test_given_may_june_beauty_growth_is_not_flagged(self):
		# GIVEN May -> June Beauty & Personal Care revenue
		previous = 35542.11
		current = 37559.07

		# WHEN evaluated
		growth = mom_growth(previous, current)
		decision = is_flagged(growth)

		# THEN it is below the threshold
		self.assertEqual(growth, 5.67)
		self.assertEqual(decision, "not_flagged")

	def test_exact_boundary_requires_escalation(self):
		# GIVEN a synthetic exact 8% boundary
		previous = 100000
		current = 108000

		# WHEN evaluated
		growth = mom_growth(previous, current)
		decision = is_flagged(growth)

		# THEN it must be held for human review
		self.assertEqual(growth, 8.0)
		self.assertEqual(decision, "escalate_exact_boundary")

	def test_corrupted_feed_returns_exact_three_errors(self):
		# GIVEN the corrupted fixture
		path = os.path.join(FIXTURES_DIR, "corrupted_feed.csv")

		# WHEN validation runs
		valid, errors = validate_feed(path)

		# THEN validation fails with exactly three errors
		expected_errors = [
			"line 3: negative revenue (-4200.0) for category=Western Wear",
			"line 4: missing category (month=July)",
			"line 6: missing revenue (category=Home & Kitchen)",
		]

		self.assertFalse(valid)
		self.assertEqual(errors, expected_errors)

	def test_part1_monthly_feed_is_valid(self):
		# GIVEN the validated Part 1 monthly revenue feed
		path = os.path.join(
			FIXTURES_DIR,
			"monthly_category_revenue.csv"
		)

		# WHEN validation runs
		valid, errors = validate_feed(path)

		# THEN all 15 rows pass
		self.assertTrue(valid)
		self.assertEqual(errors, [])


if __name__ == "__main__":
	unittest.main()
