# Meesho Reseller Growth & Alert Intelligence Pipeline

## Overview

This project is an end-to-end reseller growth-monitoring pipeline for Meesho.

The workflow connects four parts:

**Part 1 → Part 2 → Part 3 → Part 4**

- **Part 1:** SQL business queries generate verified revenue metrics.
- **Part 2:** Python validates the revenue feed and calculates Month-on-Month (MoM) growth using an 8% threshold.
- **Part 3:** Verified results are converted into stakeholder-ready narratives using deterministic templates.
- **Part 4:** A guarded mock agent connects the previous parts, validates inputs, detects significant changes, creates limited message drafts, and holds them for human approval.

The complete pipeline runs offline and requires **no API keys or paid services**.

---

## Project Structure

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── run_queries.py
└── output/

part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/

part3_narrative/
├── prompt_pack.md
├── narrative_report.md
└── masking.py
└── template_fill.py

part4_agent/
├── agent_spec.md
└── mock_agent_runner.py
└── test_mock_agent_runner.py

README.md

1. Generate the Dataset

From the project root:

python data/generate_dataset.py

This generates:

data/resellers.csv
data/orders.csv
data/meesho_reseller.db

2. Run Part 1 — SQL Business Query Engine

Run the SQL queries in:

part1_sql/run_queries.py

using:

data/meesho_reseller.db

The query results are saved under:

part1_sql/output/

The main output passed to later parts is:

part1_sql/output/monthly_category_revenue.csv

3. Run Part 2 — Growth Detection Engine

Run the tests:

python -m pytest part2_engine/test_growth_engine.py

The engine validates the revenue feed, calculates MoM growth, and applies the 8% threshold.

4. Run Part 3 — Narrative Layer

The Part 3 files are in:

part3_narrative/
prompt_pack.md contains the reusable narrative template.
narrative_report.md contains the required worked narratives and chart-choice justification.
masking.py prevents raw reseller names from appearing in external-facing narratives.
template_fill.py generates a stakeholder-ready narrative using only the verified Part 1/Part 2 values, without any external AI or API.

Part 3 uses verified results from Parts 1 and 2 and does not invent figures.

5. Run Part 4 — Mock Agent

Run the mock agent using the entry point implemented in:

part4_agent/mock_agent_runner.py

For example:

python -m part4_agent.mock_agent_runner

The agent:

Validates the input feed.
Stops if validation fails.
Calculates MoM growth.
Applies the 8% threshold.
Sorts flagged categories by absolute growth.
Drafts messages for at most the top 3 flagged categories.
Suppresses additional flagged categories for manual review.
Separately records exact 8% boundary cases for escalation.
Produces structured JSON output.
Holds all drafted messages for human approval.

No real message is automatically sent.

How the Parts Connect
Part 1
SQL Business Queries
      ↓
Verified Revenue Feed
      ↓
Part 2
Validation + MoM Growth
      ↓
Flagged Categories
      ↓
Part 3
Narrative Template + Masking
      ↓
Part 4
Guarded Agent + Human Approval

Part 1 → Part 2 follows the required order of calculating verified business numbers before applying growth rules.

Part 2 → Part 3 ensures that narratives are based only on validated numbers.

Part 3 → Part 4 allows the agent to create stakeholder-ready drafts while maintaining validation and masking safeguards.

Overall, the workflow follows:

Intake → Summary → Report Draft → Validate → Human Review

## Offline Execution

The complete pipeline works with zero API keys and requires no paid or account-gated services.

## Documentation Reference

Official Python standard-library documentation was consulted for relevant Python functionality used in this project.