import sqlite3
import random

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

# --- Add more products ---
products = [
    ("Laptop", "Electronics", 120000),
    ("Phone", "Electronics", 80000),
    ("Headphones", "Electronics", 5000),
    ("Smartwatch", "Electronics", 15000),
    ("Tablet", "Electronics", 45000),
    ("Bluetooth Speaker", "Electronics", 6000),
    ("Desk", "Furniture", 15000),
    ("Chair", "Furniture", 8000),
    ("Bookshelf", "Furniture", 12000),
    ("Sofa", "Furniture", 60000),
    ("Notebook", "Stationery", 200),
    ("Pen", "Stationery", 50),
    ("Backpack", "Stationery", 2500),
    ("Highlighter Set", "Stationery", 300),
    ("T-Shirt", "Clothing", 1500),
    ("Jeans", "Clothing", 3500),
    ("Jacket", "Clothing", 6000),
    ("Sneakers", "Clothing", 8000),
]
cur.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)
conn.commit()

# --- Get actual user and product IDs from the DB ---
cur.execute("SELECT id FROM users")
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM products")
product_ids = [row[0] for row in cur.fetchall()]

print(f"Found {len(user_ids)} users and {len(product_ids)} products")

# --- Generate ~200 random orders ---
orders = []
for _ in range(200):
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 5)
    orders.append((user_id, product_id, quantity))

cur.executemany(
    "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
    orders
)
conn.commit()
conn.close()

print(f"Inserted {len(products)} products and {len(orders)} orders successfully")