import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "mikopohub.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all MikopoHub database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------------
    # BORROWERS
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrower_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            national_id TEXT,
            location TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------------------------------
    # LOANS
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_number TEXT UNIQUE NOT NULL,
            borrower_id INTEGER NOT NULL,

            principal REAL NOT NULL,
            interest_rate REAL NOT NULL DEFAULT 20.0,

            issue_date TEXT NOT NULL,
            due_date TEXT,

            status TEXT NOT NULL DEFAULT 'ACTIVE',

            FOREIGN KEY (borrower_id)
                REFERENCES borrowers(id)
                ON DELETE RESTRICT
        )
    """)

    # ---------------------------------------
    # MONTHLY LOAN PERIODS
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_periods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER NOT NULL,

            month_start TEXT NOT NULL,
            month_end TEXT NOT NULL,

            opening_principal REAL NOT NULL,
            interest_due REAL NOT NULL,

            interest_paid REAL NOT NULL DEFAULT 0,
            principal_paid REAL NOT NULL DEFAULT 0,

            status TEXT NOT NULL DEFAULT 'ACTIVE',

            FOREIGN KEY (loan_id)
                REFERENCES loans(id)
                ON DELETE CASCADE
        )
    """)

    # ---------------------------------------
    # PAYMENTS
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            loan_id INTEGER NOT NULL,
            monthly_period_id INTEGER,

            payment_date TEXT NOT NULL,

            amount REAL NOT NULL,

            interest_portion REAL NOT NULL DEFAULT 0,
            principal_portion REAL NOT NULL DEFAULT 0,

            payment_method TEXT,
            reference_number TEXT,

            FOREIGN KEY (loan_id)
                REFERENCES loans(id)
                ON DELETE CASCADE,

            FOREIGN KEY (monthly_period_id)
                REFERENCES monthly_periods(id)
                ON DELETE SET NULL
        )
    """)

    # ---------------------------------------
    # FORM FEES
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS form_fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            borrower_id INTEGER NOT NULL,

            requested_amount REAL NOT NULL,
            fee_amount REAL NOT NULL,

            payment_status TEXT NOT NULL DEFAULT 'UNPAID',

            payment_method TEXT,
            reference_number TEXT,

            payment_date TEXT,

            FOREIGN KEY (borrower_id)
                REFERENCES borrowers(id)
                ON DELETE CASCADE
        )
    """)

    # ---------------------------------------
    # PUSH FORWARD HISTORY
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS push_forward_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            loan_id INTEGER NOT NULL,

            from_period_id INTEGER NOT NULL,
            to_period_id INTEGER NOT NULL,

            principal_carried REAL NOT NULL,

            push_date TEXT NOT NULL,

            FOREIGN KEY (loan_id)
                REFERENCES loans(id)
                ON DELETE CASCADE,

            FOREIGN KEY (from_period_id)
                REFERENCES monthly_periods(id),

            FOREIGN KEY (to_period_id)
                REFERENCES monthly_periods(id)
        )
    """)

    # ---------------------------------------
    # COLLATERAL / SECURITY
    # ---------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS collateral (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            collateral_number TEXT UNIQUE NOT NULL,

            loan_id INTEGER NOT NULL,

            security_type TEXT NOT NULL,
            description TEXT NOT NULL,

            estimated_value REAL,

            serial_number TEXT,
            condition TEXT,

            date_received TEXT,

            status TEXT NOT NULL DEFAULT 'HELD',

            notes TEXT,

            FOREIGN KEY (loan_id)
                REFERENCES loans(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("MikopoHub database initialized successfully.")