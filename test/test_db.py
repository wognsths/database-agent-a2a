import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "test.db"

ddl = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    email   TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS orders (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    product   TEXT,
    amount    REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sql_query_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    sql_query     TEXT,
    success       BOOLEAN,
    error_message TEXT,
    rows_returned INTEGER,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

dml = """
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob',   'bob@example.com');

INSERT INTO orders (user_id, product, amount) VALUES
  (1, 'Keyboard', 49.99),
  (1, 'Mouse',    19.99),
  (2, 'Monitor', 199.0);
"""

print(f"[+] Initialising {DB_PATH}")
with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(ddl)
    conn.executescript(dml)
print("[+] Done!")
