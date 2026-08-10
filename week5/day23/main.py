from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# --- Pydantic models ---
class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

# --- Helper to get DB connection ---
def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Health check ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- CREATE a user ---
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", (user.name,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "name": user.name}

# --- READ a single user ---
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row["id"], "name": row["name"]}

# --- READ all users ---
@app.get("/users")
def list_users(limit: int = 10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r["id"], "name": r["name"]} for r in rows]

# --- DELETE a user ---
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": f"User {user_id} deleted"}