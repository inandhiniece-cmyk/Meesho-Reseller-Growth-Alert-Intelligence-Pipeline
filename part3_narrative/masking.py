def alias_for(reseller_id: str) -> str:
	"""Convert RS019 -> ALIAS-19."""
	return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
	text: str,
	reseller_names: list[str],
) -> bool:
	"""Return False if any raw reseller name appears in the text."""
	return not any(name in text for name in reseller_names)


if __name__ == "__main__":
	assert alias_for("RS019") == "ALIAS-19"
	assert alias_for("RS006") == "ALIAS-06"

	safe_text = (
		"West region reseller ALIAS-19 appears in the top-reseller review."
	)

	leaked_text = (
		"West region reseller Mumbai Reseller 1 appears in the review."
	)

	names = [
		"Mumbai Reseller 1",
		"Mumbai Reseller 4",
		"Hyderabad Reseller 6",
		"Lucknow Reseller 6",
		"Jaipur Reseller 5",
	]

	assert assert_no_raw_names_leak(safe_text, names) is True
	assert assert_no_raw_names_leak(leaked_text, names) is False

	print("Masking tests passed.")
