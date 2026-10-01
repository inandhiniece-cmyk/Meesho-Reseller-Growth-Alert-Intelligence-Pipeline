def fill_growth_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Fill the approved narrative template using only verified values.

    No API, LLM, network connection, or external service is used.
    """
    return (
        f"Context: {category} revenue moved from INR "
        f"{previous_revenue:.2f} in {prev_month} to INR "
        f"{current_revenue:.2f} in {month}.\n"
        f"Insight (fact): {category} revenue changed "
        f"{mom_pct}% month-on-month from {prev_month} to {month}.\n"
        f"Implication (hypothesis): Review the {category} assortment, "
        f"seller supply, campaign mix, and regional demand signals before "
        f"deciding the next operational action."
    )
