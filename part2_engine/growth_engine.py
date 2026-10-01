import csv


REQUIRED_COLUMNS = ["month", "category", "revenue", "n_orders"]


def mom_growth(previous: float, current: float) -> float:
	"""Return Month-on-Month revenue growth percentage rounded to 2 decimals."""
	return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
	"""Classify MoM growth using the 8% threshold."""
	if abs(mom_pct) > threshold:
		return "flagged"

	if abs(mom_pct) < threshold:
		return "not_flagged"

	return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
	"""
	Validate a monthly revenue CSV.

	Expected columns:
	month,category,revenue,n_orders

	Returns:
		(True, []) when there are no validation errors.
		(False, errors) when one or more rows fail validation.
	"""
	errors = []

	with open(csv_path, "r", newline="", encoding="utf-8") as file:
		reader = csv.DictReader(file)

		for row in reader:
			line_number = reader.line_num

			month = (row.get("month") or "").strip()
			category = (row.get("category") or "").strip()
			revenue = (row.get("revenue") or "").strip()

			if not category:
				errors.append(
					f"line {line_number}: missing category (month={month})"
				)

			if not revenue:
				errors.append(
					f"line {line_number}: missing revenue (category={category})"
				)
				continue

			try:
				revenue_value = float(revenue)
			except ValueError:
				errors.append(
					f"line {line_number}: revenue not numeric: {revenue!r}"
				)
				continue

			if revenue_value < 0:
				errors.append(
					f"line {line_number}: negative revenue ({revenue_value}) "
					f"for category={category}"
				)

	return (len(errors) == 0, errors)
