import sqlite3

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

def run_query(title, query):
    print(f"\n--- {title} ---")
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)

run_query("Users with most orders", """
    SELECT u.name, COUNT(o.id) AS order_count
    FROM users u
    JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
    ORDER BY order_count DESC
    LIMIT 5;
""")

run_query("Revenue per category", """
    SELECT p.category, SUM(p.price * o.quantity) AS revenue
    FROM orders o
    JOIN products p ON o.product_id = p.id
    GROUP BY p.category
    ORDER BY revenue DESC;
""")

run_query("Average order value per user", """
    SELECT u.name, AVG(p.price * o.quantity) AS avg_order_value
    FROM orders o
    JOIN users u ON o.user_id = u.id
    JOIN products p ON o.product_id = p.id
    GROUP BY u.id
    ORDER BY avg_order_value DESC
    LIMIT 5;
""")

run_query("Most popular products", """
    SELECT p.name, SUM(o.quantity) AS total_sold
    FROM orders o
    JOIN products p ON o.product_id = p.id
    GROUP BY p.id
    ORDER BY total_sold DESC
    LIMIT 5;
""")

run_query("Users with no orders", """
    SELECT u.name
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE o.id IS NULL;
""")

conn.close()