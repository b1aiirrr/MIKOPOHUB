import sqlite3
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Optional, List

from auth import (
    ADMIN_PASSWORD_HASH,
    verify_password,
    hash_password,
    create_access_token,
    decode_access_token
)
from fastapi import FastAPI, HTTPException, Query, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="MIKOPOHUB Web API",
    version="2.1.0",
    description="Complete Micro-Lending API covering Borrowers, Loans, Push-Forward, Payments, Form Fees, Collateral, Auth & Audit Logs",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path pointing to desktop_legacy/mikopohub.db
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = (BASE_DIR.parent.parent / "desktop_legacy" / "mikopohub.db").resolve()


def get_db_connection() -> sqlite3.Connection:
    target_path = DB_PATH
    if not target_path.exists():
        local_fallback = BASE_DIR / "mikopohub.db"
        if local_fallback.exists():
            target_path = local_fallback
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Database file not found at {DB_PATH}",
            )

    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@app.on_event("startup")
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'CLIENT',
            borrower_id INTEGER,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    # Check default admin
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
            ("admin", hash_password("admin123"), "ADMIN", datetime.utcnow().isoformat())
        )
    conn.commit()
    conn.close()


def log_audit(user_id: Optional[int], username: str, action: str, entity: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (user_id, username, action, entity, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, action, entity, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def money(val) -> Decimal:
    return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generate_number(prefix: str, table: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")
    total = cursor.fetchone()["total"]
    conn.close()
    return f"{prefix}-{total + 1:04d}"


# --- Pydantic Request Models ---
class BorrowerCreateRequest(BaseModel):
    full_name: str
    phone: str
    national_id: Optional[str] = ""
    location: Optional[str] = ""


class LoanCreateRequest(BaseModel):
    borrower_id: int
    principal: float
    interest_rate: Optional[float] = 20.0
    issue_date: Optional[str] = None


class PaymentCreateRequest(BaseModel):
    loan_id: int
    amount: float
    payment_method: Optional[str] = "M-PESA Buy Goods Till"
    reference_number: Optional[str] = ""
    phone_number: Optional[str] = "254700000000"


class FormFeeCreateRequest(BaseModel):
    borrower_id: int
    requested_amount: float


class FormFeePayRequest(BaseModel):
    payment_method: Optional[str] = "M-PESA"
    reference_number: str


class CollateralCreateRequest(BaseModel):
    loan_id: int
    security_type: str
    description: str
    estimated_value: Optional[float] = 0.0
    serial_number: Optional[str] = ""
    condition: Optional[str] = "Good"
    notes: Optional[str] = ""


class CollateralUpdateRequest(BaseModel):
    status: str
    notes: Optional[str] = ""


class RegisterRequest(BaseModel):
    username: str
    email: Optional[str] = ""
    password: str
    full_name: str
    phone: str
    national_id: Optional[str] = ""


class LoginRequest(BaseModel):
    username: str  # Can be username or email
    password: str


class GoogleLoginRequest(BaseModel):
    email: str
    full_name: str
    google_id: Optional[str] = ""


class ClientLoanApplyRequest(BaseModel):
    principal: float
    purpose: Optional[str] = ""


# --- AUTH & AUDIT ENDPOINTS ---

@app.post("/api/auth/register")
def register_user(req: RegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if username or email exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR (email != '' AND email = ?)", (req.username.strip(), req.email.strip().lower()))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username or Email already registered")

        # Auto-create or link matching borrower record
        cursor.execute("SELECT id FROM borrowers WHERE phone = ? OR national_id = ? OR (email != '' AND email = ?)", (req.phone.strip(), req.national_id.strip(), req.email.strip().lower()))
        existing_b = cursor.fetchone()
        
        if existing_b:
            borrower_id = existing_b["id"]
        else:
            b_num = generate_number("BRW", "borrowers")
            cursor.execute(
                "INSERT INTO borrowers (borrower_number, full_name, phone, national_id, email) VALUES (?, ?, ?, ?, ?)",
                (b_num, req.full_name, req.phone, req.national_id, req.email.strip().lower())
            )
            borrower_id = cursor.lastrowid

        pwd_hash = hash_password(req.password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role, borrower_id, created_at) VALUES (?, ?, ?, 'CLIENT', ?, ?)",
            (req.username.strip(), req.email.strip().lower(), pwd_hash, borrower_id, datetime.utcnow().isoformat())
        )
        user_id = cursor.lastrowid
        conn.commit()

        token = create_access_token({"sub": str(user_id), "username": req.username, "email": req.email, "role": "CLIENT", "borrower_id": borrower_id})
        log_audit(user_id, req.username, "REGISTER", f"Created client account linked to Borrower #{borrower_id}")

        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user_id,
                "username": req.username,
                "email": req.email,
                "role": "CLIENT",
                "borrower_id": borrower_id
            }
        }
    finally:
        conn.close()


@app.post("/api/auth/login")
def login_user(req: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user_input = req.username.strip().lower()
        cursor.execute("SELECT * FROM users WHERE username = ? OR LOWER(email) = ?", (req.username.strip(), user_input))
        user = cursor.fetchone()

        if not user or not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid username, email, or password")

        token = create_access_token({
            "sub": str(user["id"]),
            "username": user["username"],
            "role": user["role"],
            "borrower_id": user["borrower_id"]
        })

        log_audit(user["id"], user["username"], "LOGIN", f"User logged in as {user['role']}")

        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"] if "email" in user.keys() else "",
                "role": user["role"],
                "borrower_id": user["borrower_id"]
            }
        }
    finally:
        conn.close()


@app.post("/api/auth/google-login")
def google_login_user(req: GoogleLoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        email_clean = req.email.strip().lower()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = ? OR username = ?", (email_clean, email_clean.split("@")[0]))
        user = cursor.fetchone()

        if not user:
            # Auto-register borrower
            cursor.execute("SELECT id FROM borrowers WHERE LOWER(email) = ?", (email_clean,))
            existing_b = cursor.fetchone()
            if existing_b:
                borrower_id = existing_b["id"]
            else:
                b_num = generate_number("BRW", "borrowers")
                cursor.execute(
                    "INSERT INTO borrowers (borrower_number, full_name, phone, email) VALUES (?, ?, '254700000000', ?)",
                    (b_num, req.full_name, email_clean)
                )
                borrower_id = cursor.lastrowid

            pwd_hash = hash_password(f"google_oauth_{email_clean}")
            username = email_clean.split("@")[0]
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role, borrower_id, created_at) VALUES (?, ?, ?, 'CLIENT', ?, ?)",
                (username, email_clean, pwd_hash, borrower_id, datetime.utcnow().isoformat())
            )
            user_id = cursor.lastrowid
            conn.commit()
            role = "CLIENT"
        else:
            user_id = user["id"]
            username = user["username"]
            role = user["role"]
            borrower_id = user["borrower_id"]

        token = create_access_token({"sub": str(user_id), "username": username, "email": email_clean, "role": role, "borrower_id": borrower_id})
        log_audit(user_id, username, "GOOGLE_LOGIN", f"Signed in with Gmail: {email_clean}")

        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user_id,
                "username": username,
                "email": email_clean,
                "role": role,
                "borrower_id": borrower_id
            }
        }
    finally:
        conn.close()

                "role": user["role"],
                "borrower_id": user["borrower_id"]
            }
        }
    finally:
        conn.close()


@app.get("/api/auth/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return {"authenticated": False}

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "user": {
            "id": payload.get("sub"),
            "username": payload.get("username"),
            "role": payload.get("role"),
            "borrower_id": payload.get("borrower_id")
        }
    }


@app.get("/api/admin/audit-logs")
def get_audit_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 100")
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


# --- BORROWER CLIENT PORTAL ENDPOINTS ---

@app.get("/api/client/my-loans")
def get_client_loans(borrower_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT l.*, b.full_name AS borrower_name 
            FROM loans l
            JOIN borrowers b ON l.borrower_id = b.id
            WHERE l.borrower_id = ?
            ORDER BY l.id DESC
        """, (borrower_id,))
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.get("/api/client/my-payments")
def get_client_payments(borrower_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.*, l.loan_number
            FROM payments p
            JOIN loans l ON p.loan_id = l.id
            WHERE l.borrower_id = ?
            ORDER BY p.id DESC
        """, (borrower_id,))
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


# --- DASHBOARD & CORE ENDPOINTS ---

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "MIKOPOHUB Web API",
        "version": "2.1.0",
        "features": [
            "Borrowers", "Loans", "Push-Forward", "Payments", 
            "Form Fees", "Collateral Registry", "Auth", "Audit Logs"
        ]
    }


@app.get("/api/dashboard")
def get_dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM borrowers")
        total_borrowers = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM loans WHERE status = 'ACTIVE'")
        active_loans = cursor.fetchone()["count"]

        cursor.execute("SELECT COALESCE(SUM(principal), 0.0) AS total FROM loans")
        total_lent = cursor.fetchone()["total"]

        cursor.execute("SELECT COALESCE(SUM(amount), 0.0) AS total FROM payments")
        total_repaid = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS count FROM collateral WHERE status = 'HELD'")
        held_collateral = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM form_fees WHERE payment_status = 'UNPAID'")
        unpaid_fees = cursor.fetchone()["count"]

        return {
            "total_borrowers": total_borrowers,
            "active_loans": active_loans,
            "total_lent": total_lent,
            "total_repaid": total_repaid,
            "held_collateral": held_collateral,
            "unpaid_fees": unpaid_fees,
            "currency": "KES",
        }
    finally:
        conn.close()


# BORROWERS MANAGEMENT
@app.get("/api/borrowers")
def list_borrowers(search: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT b.*, 
                   COUNT(l.id) AS total_loans,
                   SUM(CASE WHEN l.status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_loans
            FROM borrowers b
            LEFT JOIN loans l ON b.id = l.borrower_id
        """
        params = []
        if search:
            query += " WHERE b.full_name LIKE ? OR b.phone LIKE ? OR b.borrower_number LIKE ? OR b.national_id LIKE ?"
            term = f"%{search}%"
            params = [term, term, term, term]
        
        query += " GROUP BY b.id ORDER BY b.id DESC"
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.post("/api/borrowers")
def create_borrower(borrower: BorrowerCreateRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        borrower_number = generate_number("BRW", "borrowers")
        cursor.execute(
            """
            INSERT INTO borrowers (borrower_number, full_name, phone, national_id, location)
            VALUES (?, ?, ?, ?, ?)
            """,
            (borrower_number, borrower.full_name, borrower.phone, borrower.national_id, borrower.location)
        )
        borrower_id = cursor.lastrowid
        conn.commit()
        log_audit(None, "SYSTEM/ADMIN", "CREATE_BORROWER", f"Registered Borrower #{borrower_number}")
        return {
            "status": "success",
            "message": "Borrower registered successfully",
            "borrower_id": borrower_id,
            "borrower_number": borrower_number
        }
    finally:
        conn.close()


# LOANS ENGINE
@app.get("/api/loans")
def list_loans(search: Optional[str] = Query(None), status_filter: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT l.*, b.full_name AS borrower_name, b.phone AS borrower_phone, b.borrower_number
            FROM loans l
            JOIN borrowers b ON l.borrower_id = b.id
        """
        where_clauses = []
        params = []
        if search:
            where_clauses.append("(l.loan_number LIKE ? OR b.full_name LIKE ? OR b.phone LIKE ?)")
            term = f"%{search}%"
            params.extend([term, term, term])
        if status_filter:
            where_clauses.append("l.status = ?")
            params.append(status_filter)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY l.id DESC"
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.post("/api/loans")
def create_loan(loan: LoanCreateRequest):
    principal_dec = money(loan.principal)
    if principal_dec <= 0:
        raise HTTPException(status_code=400, detail="Principal must be greater than 0.")

    issue_date = date.fromisoformat(loan.issue_date) if loan.issue_date else date.today()
    due_date = issue_date + timedelta(days=30)
    interest_amount = money(principal_dec * Decimal("0.20"))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        loan_number = generate_number("LN", "loans")
        cursor.execute(
            """
            INSERT INTO loans (loan_number, borrower_id, principal, interest_rate, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE')
            """,
            (loan_number, loan.borrower_id, float(principal_dec), loan.interest_rate or 20.0, issue_date.isoformat(), due_date.isoformat())
        )
        loan_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO monthly_periods (loan_id, month_start, month_end, opening_principal, interest_due)
            VALUES (?, ?, ?, ?, ?)
            """,
            (loan_id, issue_date.isoformat(), due_date.isoformat(), float(principal_dec), float(interest_amount))
        )

        conn.commit()
        log_audit(None, "ADMIN", "ISSUE_LOAN", f"Issued Loan #{loan_number} of KES {principal_dec}")
        return {
            "status": "success",
            "message": "Loan facility issued successfully",
            "loan_id": loan_id,
            "loan_number": loan_number,
            "interest_due": float(interest_amount),
            "due_date": due_date.isoformat()
        }
    finally:
        conn.close()


# PUSH FORWARD ENGINE
@app.post("/api/loans/{loan_id}/push-forward")
def push_loan_forward(loan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
        loan = cursor.fetchone()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found.")

        cursor.execute(
            "SELECT * FROM monthly_periods WHERE loan_id = ? AND status = 'ACTIVE' ORDER BY id DESC LIMIT 1",
            (loan_id,)
        )
        period = cursor.fetchone()
        if not period:
            raise HTTPException(status_code=400, detail="No active monthly period found.")

        interest_due = Decimal(str(period["interest_due"]))
        interest_paid = Decimal(str(period["interest_paid"]))

        if interest_paid < interest_due:
            diff = float(interest_due - interest_paid)
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot push forward. Interest of KES {diff:,.2f} remains unpaid for current period."
            )

        remaining_principal = Decimal(str(loan["principal"]))
        if remaining_principal <= 0:
            raise HTTPException(status_code=400, detail="Loan principal is fully paid.")

        cursor.execute("UPDATE monthly_periods SET status = 'CARRIED_FORWARD' WHERE id = ?", (period["id"],))

        current_end = date.fromisoformat(period["month_end"])
        next_start = current_end + timedelta(days=1)
        next_end = next_start + timedelta(days=30)
        next_interest = money(remaining_principal * Decimal("0.20"))

        cursor.execute(
            """
            INSERT INTO monthly_periods (loan_id, month_start, month_end, opening_principal, interest_due, status)
            VALUES (?, ?, ?, ?, ?, 'ACTIVE')
            """,
            (loan_id, next_start.isoformat(), next_end.isoformat(), float(remaining_principal), float(next_interest))
        )
        next_period_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO push_forward_history (loan_id, from_period_id, to_period_id, principal_carried, push_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (loan_id, period["id"], next_period_id, float(remaining_principal), date.today().isoformat())
        )

        conn.commit()
        log_audit(None, "ADMIN", "PUSH_FORWARD", f"Pushed Forward Loan #{loan['loan_number']}")
        return {
            "status": "success",
            "message": "Loan period pushed forward to next month",
            "principal_carried": float(remaining_principal),
            "new_interest_due": float(next_interest),
            "next_due_date": next_end.isoformat()
        }
    finally:
        conn.close()


# PAYMENTS ENGINE
@app.get("/api/payments")
def list_payments():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT p.*, l.loan_number, b.full_name AS borrower_name
            FROM payments p
            JOIN loans l ON p.loan_id = l.id
            JOIN borrowers b ON l.borrower_id = b.id
            ORDER BY p.id DESC
            """
        )
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.post("/api/payments")
def record_payment(payment: PaymentCreateRequest):
    amount_dec = money(payment.amount)
    if amount_dec <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be greater than KES 0.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM loans WHERE id = ?", (payment.loan_id,))
        loan = cursor.fetchone()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found.")

        cursor.execute(
            "SELECT * FROM monthly_periods WHERE loan_id = ? AND status = 'ACTIVE' ORDER BY id DESC LIMIT 1",
            (payment.loan_id,)
        )
        period = cursor.fetchone()
        if not period:
            raise HTTPException(status_code=400, detail="No active monthly period found.")

        interest_due = Decimal(str(period["interest_due"]))
        interest_paid = Decimal(str(period["interest_paid"]))
        interest_remaining = max(Decimal("0.00"), interest_due - interest_paid)

        interest_allocation = min(amount_dec, interest_remaining)
        principal_allocation = amount_dec - interest_allocation

        cursor.execute(
            """
            INSERT INTO payments (
                loan_id, monthly_period_id, payment_date, amount,
                interest_portion, principal_portion, payment_method, reference_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payment.loan_id,
                period["id"],
                date.today().isoformat(),
                float(amount_dec),
                float(interest_allocation),
                float(principal_allocation),
                payment.payment_method or "M-PESA Buy Goods Till",
                payment.reference_number.strip().upper() if payment.reference_number else ""
            )
        )

        new_interest_paid = interest_paid + interest_allocation
        new_principal_paid = Decimal(str(period["principal_paid"])) + principal_allocation
        cursor.execute(
            "UPDATE monthly_periods SET interest_paid = ?, principal_paid = ? WHERE id = ?",
            (float(new_interest_paid), float(new_principal_paid), period["id"])
        )

        current_principal = Decimal(str(loan["principal"]))
        new_principal = max(Decimal("0.00"), current_principal - principal_allocation)

        if new_principal <= Decimal("0.00"):
            cursor.execute("UPDATE loans SET principal = 0, status = 'PAID' WHERE id = ?", (payment.loan_id,))
        else:
            cursor.execute("UPDATE loans SET principal = ? WHERE id = ?", (float(new_principal), payment.loan_id))

        conn.commit()
        log_audit(None, "PAYMENT_GATEWAY", "RECORD_PAYMENT", f"Allocated KES {amount_dec} for Loan #{loan['loan_number']}")
        return {
            "status": "success",
            "message": "Payment allocated successfully",
            "allocated_interest": float(interest_allocation),
            "allocated_principal": float(principal_allocation),
            "remaining_principal": float(new_principal),
            "loan_status": "PAID" if new_principal <= Decimal("0.00") else "ACTIVE"
        }
    finally:
        conn.close()


# FORM FEES
@app.get("/api/form-fees")
def list_form_fees():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT f.*, b.full_name AS borrower_name, b.phone, b.borrower_number
            FROM form_fees f
            JOIN borrowers b ON f.borrower_id = b.id
            ORDER BY f.id DESC
            """
        )
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.post("/api/form-fees")
def create_form_fee(fee: FormFeeCreateRequest):
    req_amt = money(fee.requested_amount)
    fee_amt = Decimal("500.00") if req_amt <= 50000 else Decimal("1000.00")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO form_fees (borrower_id, requested_amount, fee_amount) VALUES (?, ?, ?)",
            (fee.borrower_id, float(req_amt), float(fee_amt))
        )
        fee_id = cursor.lastrowid
        conn.commit()
        return {"status": "success", "fee_id": fee_id, "fee_amount": float(fee_amt)}
    finally:
        conn.close()


@app.post("/api/form-fees/{fee_id}/pay")
def pay_form_fee(fee_id: int, pay_data: FormFeePayRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE form_fees
            SET payment_status = 'PAID', payment_method = ?, reference_number = ?, payment_date = ?
            WHERE id = ?
            """,
            (pay_data.payment_method, pay_data.reference_number.strip().upper(), date.today().isoformat(), fee_id)
        )
        conn.commit()
        return {"status": "success", "message": "Form fee marked as PAID"}
    finally:
        conn.close()


# COLLATERAL REGISTRY
@app.get("/api/collateral")
def list_collateral(search: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT c.*, l.loan_number, b.full_name AS borrower_name
            FROM collateral c
            JOIN loans l ON c.loan_id = l.id
            JOIN borrowers b ON l.borrower_id = b.id
        """
        params = []
        if search:
            query += " WHERE c.collateral_number LIKE ? OR c.security_type LIKE ? OR c.description LIKE ? OR c.serial_number LIKE ?"
            term = f"%{search}%"
            params = [term, term, term, term]

        query += " ORDER BY c.id DESC"
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return {"status": "success", "data": rows}
    finally:
        conn.close()


@app.post("/api/collateral")
def create_collateral(item: CollateralCreateRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        collateral_number = generate_number("COL", "collateral")
        cursor.execute(
            """
            INSERT INTO collateral (
                collateral_number, loan_id, security_type, description,
                estimated_value, serial_number, condition, date_received, status, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'HELD', ?)
            """,
            (
                collateral_number, item.loan_id, item.security_type, item.description,
                item.estimated_value or 0.0, item.serial_number, item.condition or "Good",
                date.today().isoformat(), item.notes
            )
        )
        item_id = cursor.lastrowid
        conn.commit()
        return {
            "status": "success",
            "message": "Collateral registered successfully",
            "collateral_id": item_id,
            "collateral_number": collateral_number
        }
    finally:
        conn.close()


@app.put("/api/collateral/{item_id}")
def update_collateral(item_id: int, update_data: CollateralUpdateRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE collateral SET status = ?, notes = ? WHERE id = ?",
            (update_data.status, update_data.notes, item_id)
        )
        conn.commit()
        return {"status": "success", "message": f"Collateral status updated to {update_data.status}"}
    finally:
        conn.close()
