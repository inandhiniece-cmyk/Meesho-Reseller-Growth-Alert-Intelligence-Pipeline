# Agent Specification

## Goal

Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any drafted message is considered sent.

## Tools

The agent calls:

1. `validate_feed()` from Part 2.
2. `mom_growth()` from Part 2.
3. `is_flagged()` from Part 2.
4. `fill_growth_template()` from Part 3.
5. `alias_for()` / `assert_no_raw_names_leak()` from Part 3 when reseller information is included in a narrative.

The Part 2 functions are imported and reused without re-implementation.

## Memory / State

The agent needs the previous month's verified revenue per category so that it can calculate the next month's MoM growth.

The verified monthly revenue feed acts as the persisted analytical state between runs.

## Planner

The agent executes these subtasks in order:

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, Hard Stop and report the validation errors.
3. If validation passes, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft a message for at most the top 3 flagged categories using the Part 3 template.
7. Log any remaining flagged categories beyond the top 3 as `suppressed, review manually` without drafting a message.
7b. Separately log any category classified as `escalate_exact_boundary` into `escalated_categories` without drafting a message.
8. Emit one structured JSON object for the run.

## Feedback Loop

Every drafted message is held for human approval. The mock runner does not send email, call an API, or perform any real external action.

The output action is therefore:

`drafted_and_held_for_approval`

rather than a send operation.

## Input Guardrail

`validate_feed` must pass before any MoM calculation or message drafting occurs.

If validation fails, the run immediately becomes a Hard Stop.

## Action Guardrail

No message is ever automatically sent.

Messages are drafted and held for human approval only.

## Output Guardrail

Every number in a drafted message must trace back to a verified Part 1 or Part 2 value.

No invented revenue, growth rate, order count, or other numeric value is permitted.

## Success Condition

A successful run produces drafts for the top flagged categories, or correctly produces zero drafts when no category crosses the threshold.

Every number in every draft must be traceable to verified inputs.

## Error Condition

If `validate_feed` returns `False`, the run is a Hard Stop.

The validation errors must be surfaced in the structured output.

No MoM calculations or drafts are produced after a validation failure.

---

# Given-When-Then Agent Specifications

## Case 1 — April to May Ethnic Wear

**Given** April → May Ethnic Wear revenue moves from 104520.77 to 185107.61,

**When** `mom_growth` then `is_flagged` run on it,

**Then** `mom_growth` returns 77.1 and `is_flagged` returns `"flagged"`.

## Case 2 — May to June Beauty & Personal Care

**Given** May → June Beauty & Personal Care revenue moves from 35542.11 to 37559.07,

**When** the agent evaluates it,

**Then** `mom_growth` returns 5.67 and `is_flagged` returns `"not_flagged"`.

## Case 3 — Exact Boundary

**Given** a synthetic pair previous=100000, current=108000,

**When** the agent evaluates it,

**Then** `mom_growth` returns exactly 8.0 and `is_flagged` returns `"escalate_exact_boundary"`.

## Case 4 — Corrupted Feed

**Given** the corrupted feed fixture,

**When** `validate_feed` runs on it,

**Then** validation returns `False` and the agent Hard Stops with exactly the three required validation errors.
