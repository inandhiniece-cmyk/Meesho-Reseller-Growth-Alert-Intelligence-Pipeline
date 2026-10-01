import csv
import json
import sys
from pathlib import Path


# Make the repository root importable when this file is run directly.
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))


from part2_engine.growth_engine import (
	is_flagged,
	mom_growth,
	validate_feed,
)

from part3_narrative.template_fill import fill_growth_template


MONTH_ORDER = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]


def previous_month_name(month: str) -> str:
	"""Return the calendar month immediately before month."""
	index = MONTH_ORDER.index(month)

	if index == 0:
		raise ValueError("January does not have a previous month in this runner.")

	return MONTH_ORDER[index - 1]


def load_rows(csv_path: str) -> list[dict]:
	"""Load the CSV into dictionaries."""
	with open(csv_path, "r", newline="", encoding="utf-8") as file:
		return list(csv.DictReader(file))


def rows_for_month(rows: list[dict], month: str) -> dict[str, dict]:
	"""
	Return category -> row for the requested month.
	"""
	result = {}

	for row in rows:
		if row["month"].strip() == month:
			result[row["category"].strip()] = row

	return result


def run(
	month: str,
	previous_month_csv: str,
	current_month_csv: str,
) -> dict:
	"""
	Run the guarded growth-monitoring workflow.

	The function returns exactly the structured output schema required
	by Part 4.
	"""

	# ------------------------------------------------------------
	# 1. Validate current feed before any analytical work.
	# ------------------------------------------------------------
	current_valid, current_errors = validate_feed(current_month_csv)

	if not current_valid:
		result = {
			"run_month": month,
			"validation_status": "invalid",
			"validation_errors": current_errors,
			"flagged_categories": [],
			"suppressed_categories": [],
			"escalated_categories": [],
			"action_taken": "hard_stop",
		}

		return result

	# Also validate the previous feed.
	previous_valid, previous_errors = validate_feed(previous_month_csv)

	if not previous_valid:
		result = {
			"run_month": month,
			"validation_status": "invalid",
			"validation_errors": previous_errors,
			"flagged_categories": [],
			"suppressed_categories": [],
			"escalated_categories": [],
			"action_taken": "hard_stop",
		}

		return result

	# ------------------------------------------------------------
	# 2. Determine previous month.
	# ------------------------------------------------------------
	prev_month = previous_month_name(month)

	# ------------------------------------------------------------
	# 3. Load verified feeds.
	# ------------------------------------------------------------
	previous_rows = load_rows(previous_month_csv)
	current_rows = load_rows(current_month_csv)

	previous = rows_for_month(previous_rows, prev_month)
	current = rows_for_month(current_rows, month)

	# ------------------------------------------------------------
	# 4. Compute MoM and classification for every category.
	# ------------------------------------------------------------
	flagged = []
	escalated_categories = []

	for category, current_row in current.items():
		if category not in previous:
			continue

		previous_revenue = float(previous[category]["revenue"])
		current_revenue = float(current_row["revenue"])

		mom_pct = mom_growth(previous_revenue, current_revenue)
		decision = is_flagged(mom_pct)

		item = {
			"category": category,
			"mom_pct": mom_pct,
			"previous_revenue": previous_revenue,
			"current_revenue": current_revenue,
		}

		if decision == "flagged":
			flagged.append(item)

		elif decision == "escalate_exact_boundary":
			escalated_categories.append(category)

	# ------------------------------------------------------------
	# 5. Sort flagged categories by absolute growth descending.
	# ------------------------------------------------------------
	flagged.sort(
		key=lambda item: abs(item["mom_pct"]),
		reverse=True,
	)

	# ------------------------------------------------------------
	# 6. Draft at most top 3.
	# ------------------------------------------------------------
	top_three = flagged[:3]
	remaining = flagged[3:]

	flagged_output = []

	for item in top_three:
		message = fill_growth_template(
			category=item["category"],
			previous_revenue=item["previous_revenue"],
			current_revenue=item["current_revenue"],
			mom_pct=item["mom_pct"],
			month=month,
			prev_month=prev_month,
		)

		flagged_output.append(
			{
				"category": item["category"],
				"mom_pct": item["mom_pct"],
				"previous_revenue": item["previous_revenue"],
				"current_revenue": item["current_revenue"],
				"drafted": True,
				"message": message,
			}
		)

	# ------------------------------------------------------------
	# 7. Suppress remaining flagged categories.
	# ------------------------------------------------------------
	suppressed_categories = [
		item["category"]
		for item in remaining
	]

	# ------------------------------------------------------------
	# 8. Emit structured JSON-compatible object.
	# ------------------------------------------------------------
	action_taken = (
		"drafted_and_held_for_approval"
		if flagged_output
		else "drafted_and_held_for_approval"
	)

	result = {
		"run_month": month,
		"validation_status": "valid",
		"validation_errors": [],
		"flagged_categories": flagged_output,
		"suppressed_categories": suppressed_categories,
		"escalated_categories": escalated_categories,
		"action_taken": action_taken,
	}

	return result


def main():
	"""Run May, June, and corrupted-feed demonstrations."""

	monthly_feed = (
		ROOT
		/ "part1_sql"
		/ "output"
		/ "monthly_category_revenue.csv"
	)

	corrupted_feed = (
		ROOT
		/ "part2_engine"
		/ "fixtures"
		/ "corrupted_feed.csv"
	)

	may_result = run(
		"May",
		str(monthly_feed),
		str(monthly_feed),
	)

	june_result = run(
		"June",
		str(monthly_feed),
		str(monthly_feed),
	)

	invalid_result = run(
		"July",
		str(monthly_feed),
		str(corrupted_feed),
	)

	print("MAY SCENARIO")
	print(json.dumps(may_result, indent=2))

	print("\nJUNE SCENARIO")
	print(json.dumps(june_result, indent=2))

	print("\nCORRUPTED FEED SCENARIO")
	print(json.dumps(invalid_result, indent=2))


if __name__ == "__main__":
	main()
