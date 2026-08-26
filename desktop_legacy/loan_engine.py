from decimal import Decimal, ROUND_HALF_UP


MONTHLY_INTEREST_RATE = Decimal("0.20")


def money(value):
    """Convert a value to money rounded to 2 decimal places."""
    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def calculate_monthly_interest(principal):
    """Calculate 20% monthly interest on the current principal."""
    principal = money(principal)
    return money(principal * MONTHLY_INTEREST_RATE)


def calculate_form_fee(loan_amount):
    """
    Calculate the borrower form fee.

    KSh 1 - 1,000      -> KSh 200
    KSh 1,001 - 5,000  -> KSh 500
    Above KSh 5,000     -> KSh 1,000
    """
    amount = money(loan_amount)

    if amount <= Decimal("1000"):
        return Decimal("200.00")

    elif amount <= Decimal("5000"):
        return Decimal("500.00")

    else:
        return Decimal("1000.00")


def allocate_payment(payment_amount, interest_due, principal):
    """
    Allocate a payment in this order:

    1. Outstanding interest
    2. Principal
    """

    payment = money(payment_amount)
    interest_due = money(interest_due)
    principal = money(principal)

    # Payment goes to interest first
    interest_payment = min(payment, interest_due)

    remaining_payment = payment - interest_payment

    # Anything left goes toward principal
    principal_payment = min(remaining_payment, principal)

    remaining_interest = interest_due - interest_payment
    remaining_principal = principal - principal_payment

    return {
        "interest_paid": money(interest_payment),
        "principal_paid": money(principal_payment),
        "remaining_interest": money(remaining_interest),
        "remaining_principal": money(remaining_principal),
    }


def can_push_forward(interest_due, interest_paid):
    """
    A borrower can carry the principal forward only
    when the current month's interest has been fully paid.
    """

    interest_due = money(interest_due)
    interest_paid = money(interest_paid)

    return interest_paid >= interest_due
if __name__ == "__main__":

    principal = Decimal("10000")

    print("MikopoHub Loan Engine Test")
    print("--------------------------")

    interest = calculate_monthly_interest(principal)

    print(f"Principal: KSh {principal:,.2f}")
    print(f"Monthly interest: KSh {interest:,.2f}")

    result = allocate_payment(
        payment_amount=3000,
        interest_due=interest,
        principal=principal
    )

    print(f"Interest paid: KSh {result['interest_paid']:,.2f}")
    print(f"Principal paid: KSh {result['principal_paid']:,.2f}")
    print(f"Remaining interest: KSh {result['remaining_interest']:,.2f}")
    print(f"Remaining principal: KSh {result['remaining_principal']:,.2f}")

    print()
    print("Form fee for KSh 5,000:",
          f"KSh {calculate_form_fee(5000):,.2f}")

    print("Can push forward:",
          can_push_forward(interest, result["interest_paid"]))