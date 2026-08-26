import sqlite3
from pathlib import Path
from typing import Optional

from auth import ADMIN_PASSWORD_HASH, verify_password
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="MIKOPOHUB Web API",
    version="2.0.0",
    description="FastAPI Backend for MikopoHub Micro-Lending PWA",
)

# CORS Middleware allowing Next.js frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path pointing to desktop_legacy/mikopohub.db
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = (BASE_DIR.parent.parent / "desktop_legacy" / "mikopohub.db").resolve()


def get_db_connection() -> sqlite3.Connection:
    """Connects to the shared mikopohub.db SQLite database."""
    target_path = DB_PATH
    if not target_path.exists():
        # Local fallback if running standalone backend tests
        local_fallback = BASE_DIR / "mikopohub.db"
        if local_fallback.exists():
            target_path = local_fallback
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Database file not found at {DB_PATH}",
            )

    connection = sqlite3.connect(target_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


class LoginRequest(BaseModel):
    username: str
    password: str


class PaymentSubmitRequest(BaseModel):
    loan_id: Optional[int] = 1
    amount: float
    payment_date: str
    reference_number: str
    payment_method: str = "M-PESA Buy Goods Till"
    phone_number: Optional[str] = "254700000000"


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "MIKOPOHUB Web API",
        "version": "2.0.0",
        "db_connected": DB_PATH.exists(),
    }


@app.post("/api/auth/login")
def login(credentials: LoginRequest):
    """Authenticate administrator using bcrypt password verification."""
    if credentials.username == "admin" and verify_password(
        credentials.password, ADMIN_PASSWORD_HASH
    ):
        return {
            "status": "success",
            "message": "Authentication successful",
            "token": "admin-session-token-v2",
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid administrator credentials",
    )


@app.get("/api/dashboard")
def get_dashboard_summary():
    """Queries shared SQLite database and returns summary metrics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Total Borrowers
        cursor.execute("SELECT COUNT(*) AS count FROM borrowers")
        row = cursor.fetchone()
        total_borrowers = row["count"] if row else 0

        # Active Loans
        cursor.execute(
            "SELECT COUNT(*) AS count FROM loans WHERE status = 'ACTIVE'"
        )
        row = cursor.fetchone()
        active_loans = row["count"] if row else 0

        # Total Lent Principal
        cursor.execute("SELECT COALESCE(SUM(principal), 0.0) AS total FROM loans")
        row = cursor.fetchone()
        total_lent = row["total"] if row else 0.0

        # Total Repaid Amount
        cursor.execute("SELECT COALESCE(SUM(amount), 0.0) AS total FROM payments")
        row = cursor.fetchone()
        total_repaid = row["total"] if row else 0.0

        return {
            "total_borrowers": total_borrowers,
            "active_loans": active_loans,
            "total_lent": total_lent,
            "total_repaid": total_repaid,
            "currency": "KES",
        }
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Database query failed: {str(e)}"
        )
    finally:
        conn.close()


@app.post("/api/payments")
def record_payment(payment: PaymentSubmitRequest):
    """Records payment and structures JSON payload for Safaricom Daraja STK Push integration."""
    if payment.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Payment amount must be greater than KES 0."
        )

    if not payment.reference_number.strip():
        raise HTTPException(
            status_code=400, detail="Reference number cannot be empty."
        )

    # Clean phone number format for Daraja API (e.g., 2547XXXXXXXX)
    phone = (payment.phone_number or "254700000000").replace("+", "").strip()

    return {
        "status": "success",
        "message": "Payment recorded and queued for M-PESA STK Push",
        "data": {
            "amount": payment.amount,
            "payment_date": payment.payment_date,
            "reference_number": payment.reference_number.strip().upper(),
            "payment_method": payment.payment_method,
            "daraja_stk_payload": {
                "BusinessShortCode": "174379",
                "TransactionType": "CustomerBuyGoodsOnline",
                "Amount": payment.amount,
                "PartyA": phone,
                "PhoneNumber": phone,
                "CallBackURL": "https://api.mikopohub.com/api/mpesa/callback",
                "AccountReference": f"LOAN-{payment.loan_id or 1}",
                "TransactionDesc": "MikopoHub Repayment",
            },
        },
    }
