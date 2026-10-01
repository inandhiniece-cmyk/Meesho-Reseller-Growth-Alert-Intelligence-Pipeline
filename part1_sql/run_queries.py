import sqlite3
import csv
import os

# Path to the SQLite database
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "meesho_reseller.db"
)

# Output folder
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "output"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ---------------------------------------------------------
# QUERY 1
# Monthly revenue by category
# ---------------------------------------------------------

query1 = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;
"""

cursor.execute(query1)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "monthly_category_revenue.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(rows)

print("Query 1 completed:")
print(output_file)


# ---------------------------------------------------------
# QUERY 2
# Region-wise total revenue and order count
# ---------------------------------------------------------

query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;
"""

cursor.execute(query2)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "region_revenue.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "revenue", "n_orders"])
    writer.writerows(rows)

print("Query 2 completed:")
print(output_file)


# ---------------------------------------------------------
# QUERY 3
# Top 5 resellers with total spend above 50,000
# ---------------------------------------------------------

query3 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name,
    r.region
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

cursor.execute(query3)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "top_resellers.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["reseller_id", "reseller_name", "region", "total_spend"]
    )
    writer.writerows(rows)

print("Query 3 completed:")
print(output_file)


# ---------------------------------------------------------
# QUERY 4
# Resellers who have never placed an order
# ---------------------------------------------------------

query4 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

cursor.execute(query4)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "zero_order_resellers.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["reseller_id", "reseller_name", "region"]
    )
    writer.writerows(rows)

print("Query 4 completed:")
print(output_file)


# ---------------------------------------------------------
# QUERY 4B
# Demonstrate COUNT(*) vs COUNT(order_id)
# ---------------------------------------------------------

query4b = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS row_count,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY
    r.reseller_id,
    r.reseller_name;
"""

cursor.execute(query4b)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "left_join_count_check.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["reseller_id", "reseller_name", "row_count", "order_count"]
    )
    writer.writerows(rows)

print("Query 4B completed:")
print(output_file)


# ---------------------------------------------------------
# QUERY 5
# June AOV for Delivered orders only
# ---------------------------------------------------------

query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

cursor.execute(query5)
rows = cursor.fetchall()

output_file = os.path.join(
    OUTPUT_DIR,
    "june_aov.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["june_delivered_aov"])
    writer.writerows(rows)

print("Query 5 completed:")
print(output_file)


# Close database connection
conn.close()

print("\nAll Part 1 queries completed successfully!")
