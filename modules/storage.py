"""
Module de stockage local (SQLite) pour le fonctionnement en mode Edge (hors-ligne).
Local storage module (SQLite) for offline / Edge Computing operation.

Toutes les fiches EFA saisies sont enregistrées localement dans data/agro_ia_cacao.db,
ce qui permet à l'agent de fonctionner sans connexion Internet.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "agro_ia_cacao.db")


def _ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS efa_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_efa TEXT UNIQUE,
            created_at TEXT,
            updated_at TEXT,
            data_json TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_efa(code_efa: str, data: dict):
    """Save or update an EFA record (identified by its unique code)."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    data_json = json.dumps(data, ensure_ascii=False)

    cur.execute("SELECT id FROM efa_records WHERE code_efa = ?", (code_efa,))
    existing = cur.fetchone()
    if existing:
        cur.execute(
            "UPDATE efa_records SET data_json = ?, updated_at = ? WHERE code_efa = ?",
            (data_json, now, code_efa),
        )
    else:
        cur.execute(
            "INSERT INTO efa_records (code_efa, created_at, updated_at, data_json) VALUES (?, ?, ?, ?)",
            (code_efa, now, now, data_json),
        )
    conn.commit()
    conn.close()


def list_efa_codes():
    """Return list of all saved EFA codes."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT code_efa FROM efa_records ORDER BY updated_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def load_efa(code_efa: str):
    """Load an EFA record by code; returns dict or None."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT data_json FROM efa_records WHERE code_efa = ?", (code_efa,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None


def delete_efa(code_efa: str):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM efa_records WHERE code_efa = ?", (code_efa,))
    conn.commit()
    conn.close()
