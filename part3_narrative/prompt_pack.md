# Reusable Prompt Pack — Reseller Growth Narrative

## Trigger

Start this prompt only when a category's `is_flagged` result is `"flagged"`.

## Input list

The prompt requires these verified placeholders:

- `{category}`
- `{previous_revenue}`
- `{current_revenue}`
- `{mom_pct}`
- `{month}`
- `{prev_month}`

All values must come from the validated Part 1 / Part 2 pipeline.

## Prompt

You are drafting a stakeholder update for a Meesho regional manager.

Use the following verified inputs:

- Category: [{category}]
- Previous month: [{prev_month}]
- Current month: [{month}]
- Previous revenue: [{previous_revenue}]
- Current revenue: [{current_revenue}]
- MoM growth: [{mom_pct}]%

Write the update using exactly this structure:

### Context
State what category revenue is being measured and compare the current month with the previous month.

### Insight
State the supplied MoM percentage as a fact.

### Implication
Give one specific, actionable next step for the regional manager. If you suggest a possible cause that is not proven by the supplied data, label it explicitly as a hypothesis.

Do not invent, estimate, round differently, or introduce any number that is not one of the supplied numeric placeholders. Do not invent reseller names, causes, order counts, or revenue figures.

## Checklist

Before the draft is used, verify:

1. Every numeric value in the draft matches a supplied numeric placeholder exactly.
2. The MoM percentage appears exactly as supplied.
3. Every data-supported statement is labeled as a fact where appropriate.
4. Any proposed cause or explanation is explicitly labeled as a hypothesis.
5. The recommendation is specific and actionable rather than vague.
6. Any reseller reference uses a coded alias rather than a raw reseller name.
7. The category and month comparison match the supplied inputs.
