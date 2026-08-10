import sqlite3
import random

conn = sqlite3.connect("shop.db")
cur = conn.cursor()

first_names = [
    "Ali", "Sara", "Bilal", "Ayesha", "Hamza", "Zainab", "Usman", "Fatima",
    "Ahmed", "Mariam", "Hassan", "Amna", "Bilawal", "Hira", "Faisal", "Sadia",
    "Imran", "Nida", "Kashif", "Rabia", "Waqar", "Sana", "Junaid", "Iqra",
    "Tariq", "Mahnoor", "Adeel", "Komal", "Shahzad", "Anum", "Farhan", "Laiba",
    "Nabeel", "Areeba", "Asad", "Warda", "Zeeshan", "Mehak", "Danish", "Noor",
    "Umer", "Zara", "Rizwan", "Alishba", "Salman", "Aiman", "Yasir", "Maham",
    "Rehan", "Sidra"
]

last_names = [
    "Khan", "Ahmed", "Malik", "Raza", "Chaudhry", "Iqbal", "Sheikh", "Butt",
    "Qureshi", "Baig", "Mirza", "Awan", "Abbasi", "Farooq", "Hashmi", "Javed",
    "Aslam", "Nawaz", "Yousaf", "Siddiqui"
]

users = []
used_names = set()

while len(users) < 100:
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    if name not in used_names:
        used_names.add(name)
        users.append((name,))

cur.executemany("INSERT INTO users (name) VALUES (?)", users)

conn.commit()
conn.close()
print(f"Inserted {len(users)} users successfully")