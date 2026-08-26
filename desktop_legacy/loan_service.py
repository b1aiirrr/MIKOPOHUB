from datetime import date, timedelta
from decimal import Decimal

from database import get_connection
from loan_engine import (
    calculate_monthly_interest,
    calculate_form_fee,
    allocate_payment,
    can_push_forward,
    money,
)


def generate_number(prefix, table, column):
    """Generate IDs such as BRW-0001 or LN-0001."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) AS total FROM {table}"
    )

    total = cursor.fetchone()["total"]
    connection.close()

    return f"{prefix}-{total + 1:04d}"


def add_borrower(
    full_name,
    phone,
    national_id="",
    location=""
):
    """Create a new borrower."""

    borrower_number = generate_number(
        "BRW",
        "borrowers",
        "borrower_number"
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO borrowers (
            borrower_number,
            full_name,
            phone,
            national_id,
            location
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            borrower_number,
            full_name,
            phone,
            national_id,
            location
        )
    )

    borrower_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return borrower_id, borrower_number


def create_form_fee(
    borrower_id,
    requested_amount
):
    """Create the required form fee for a borrower."""

    requested_amount = money(requested_amount)
    fee_amount = calculate_form_fee(requested_amount)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO form_fees (
            borrower_id,
            requested_amount,
            fee_amount
        )
        VALUES (?, ?, ?)
        """,
        (
            borrower_id,
            float(requested_amount),
            float(fee_amount)
        )
    )

    fee_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return fee_id, fee_amount


def mark_form_fee_paid(
    fee_id,
    payment_method="M-Pesa",
    reference_number=""
):
    """Mark a form fee as paid."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE form_fees
        SET
            payment_status = 'PAID',
            payment_method = ?,
            reference_number = ?,
            payment_date = ?
        WHERE id = ?
        """,
        (
            payment_method,
            reference_number,
            date.today().isoformat(),
            fee_id
        )
    )

    connection.commit()
    connection.close()


def create_loan(
    borrower_id,
    principal,
    issue_date=None
):
    """
    Create a new loan.

    The loan starts with 20% monthly interest.
    """

    principal = money(principal)

    if issue_date is None:
        issue_date = date.today()

    loan_number = generate_number(
        "LN",
        "loans",
        "loan_number"
    )

    due_date = issue_date + timedelta(days=30)

    interest = calculate_monthly_interest(principal)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO loans (
            loan_number,
            borrower_id,
            principal,
            interest_rate,
            issue_date,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            loan_number,
            borrower_id,
            float(principal),
            20.0,
            issue_date.isoformat(),
            due_date.isoformat(),
            "ACTIVE"
        )
    )

    loan_id = cursor.lastrowid

    # Create the first monthly period
    cursor.execute(
        """
        INSERT INTO monthly_periods (
            loan_id,
            month_start,
            month_end,
            opening_principal,
            interest_due
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            loan_id,
            issue_date.isoformat(),
            due_date.isoformat(),
            float(principal),
            float(interest)
        )
    )

    connection.commit()
    connection.close()

    return loan_id, loan_number, interest


def get_current_period(loan_id):
    """Get the active monthly period for a loan."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM monthly_periods
        WHERE loan_id = ?
        AND status = 'ACTIVE'
        ORDER BY id DESC
        LIMIT 1
        """,
        (loan_id,)
    )

    period = cursor.fetchone()

    connection.close()

    return period


def record_payment(
    loan_id,
    amount,
    payment_method="M-Pesa",
    reference_number=""
):
    """
    Record a payment.

    Payment priority:
    1. Interest
    2. Principal
    """

    amount = money(amount)

    connection = get_connection()
    cursor = connection.cursor()

    # Get the loan
    cursor.execute(
        """
        SELECT *
        FROM loans
        WHERE id = ?
        """,
        (loan_id,)
    )

    loan = cursor.fetchone()

    if loan is None:
        connection.close()
        raise ValueError("Loan not found.")

    # Get current monthly period
    cursor.execute(
        """
        SELECT *
        FROM monthly_periods
        WHERE loan_id = ?
        AND status = 'ACTIVE'
        ORDER BY id DESC
        LIMIT 1
        """,
        (loan_id,)
    )

    period = cursor.fetchone()

    if period is None:
        connection.close()
        raise ValueError("No active monthly period found.")

    result = allocate_payment(
        amount,
        period["interest_due"] - period["interest_paid"],
        loan["principal"]
    )

    interest_paid = result["interest_paid"]
    principal_paid = result["principal_paid"]

    # Record payment
    cursor.execute(
        """
        INSERT INTO payments (
            loan_id,
            monthly_period_id,
            payment_date,
            amount,
            interest_portion,
            principal_portion,
            payment_method,
            reference_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            loan_id,
            period["id"],
            date.today().isoformat(),
            float(amount),
            float(interest_paid),
            float(principal_paid),
            payment_method,
            reference_number
        )
    )

    # Update monthly period
    new_interest_paid = (
        Decimal(str(period["interest_paid"]))
        + interest_paid
    )

    new_principal_paid = (
        Decimal(str(period["principal_paid"]))
        + principal_paid
    )

    cursor.execute(
        """
        UPDATE monthly_periods
        SET
            interest_paid = ?,
            principal_paid = ?
        WHERE id = ?
        """,
        (
            float(new_interest_paid),
            float(new_principal_paid),
            period["id"]
        )
    )

    # Update loan principal
    new_principal = (
        Decimal(str(loan["principal"]))
        - principal_paid
    )

    cursor.execute(
        """
        UPDATE loans
        SET principal = ?
        WHERE id = ?
        """,
        (
            float(new_principal),
            loan_id
        )
    )

    # Automatically close loan if principal is fully paid
    if new_principal <= Decimal("0.00"):
        cursor.execute(
            """
            UPDATE loans
            SET
                principal = 0,
                status = 'PAID'
            WHERE id = ?
            """,
            (loan_id,)
        )

    connection.commit()
    connection.close()

    return result


def push_forward(loan_id):
    """
    Carry the remaining principal into the next month.

    The current month's interest MUST be fully paid.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM loans
        WHERE id = ?
        """,
        (loan_id,)
    )

    loan = cursor.fetchone()

    if loan is None:
        connection.close()
        raise ValueError("Loan not found.")

    cursor.execute(
        """
        SELECT *
        FROM monthly_periods
        WHERE loan_id = ?
        AND status = 'ACTIVE'
        ORDER BY id DESC
        LIMIT 1
        """,
        (loan_id,)
    )

    current = cursor.fetchone()

    if current is None:
        connection.close()
        raise ValueError("No active monthly period.")

    if not can_push_forward(
        current["interest_due"],
        current["interest_paid"]
    ):
        connection.close()
        raise ValueError(
            "Cannot push forward. "
            "The current month's interest has not been fully paid."
        )

    principal = money(loan["principal"])

    if principal <= 0:
        connection.close()
        raise ValueError("Loan has no remaining principal.")

    # Close current period
    cursor.execute(
        """
        UPDATE monthly_periods
        SET status = 'CARRIED_FORWARD'
        WHERE id = ?
        """,
        (current["id"],)
    )

    current_end = date.fromisoformat(current["month_end"])
    next_start = current_end + timedelta(days=1)
    next_end = next_start + timedelta(days=30)

    next_interest = calculate_monthly_interest(principal)

    # Create next period
    cursor.execute(
        """
        INSERT INTO monthly_periods (
            loan_id,
            month_start,
            month_end,
            opening_principal,
            interest_due,
            status
        )
        VALUES (?, ?, ?, ?, ?, 'ACTIVE')
        """,
        (
            loan_id,
            next_start.isoformat(),
            next_end.isoformat(),
            float(principal),
            float(next_interest)
        )
    )

    next_period_id = cursor.lastrowid

    # Record push-forward
    cursor.execute(
        """
        INSERT INTO push_forward_history (
            loan_id,
            from_period_id,
            to_period_id,
            principal_carried,
            push_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            loan_id,
            current["id"],
            next_period_id,
            float(principal),
            date.today().isoformat()
        )
    )

    connection.commit()
    connection.close()

    return {
        "principal_carried": principal,
        "new_monthly_interest": next_interest,
        "next_period_id": next_period_id
    }