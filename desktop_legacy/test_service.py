from loan_service import (
    add_borrower,
    create_form_fee,
    mark_form_fee_paid,
    create_loan,
    record_payment,
    push_forward
)


print("\n=== MIKOPOHUB SERVICE TEST ===\n")


# 1. Add borrower
borrower_id, borrower_number = add_borrower(
    full_name="John Doe",
    phone="0712345678",
    national_id="12345678",
    location="Kiambu"
)

print("Borrower created:")
print(borrower_number)


# 2. Create form fee
fee_id, fee = create_form_fee(
    borrower_id,
    5000
)

print("\nForm fee:")
print(f"KSh {fee:,.2f}")


# 3. Mark form fee paid
mark_form_fee_paid(
    fee_id,
    payment_method="M-Pesa",
    reference_number="TEST123"
)

print("Form fee: PAID")


# 4. Create loan
loan_id, loan_number, interest = create_loan(
    borrower_id,
    10000
)

print("\nLoan created:")
print(loan_number)

print(f"Principal: KSh 10,000.00")
print(f"Monthly interest: KSh {interest:,.2f}")


# 5. Record KSh 3,000 payment
result = record_payment(
    loan_id,
    3000,
    payment_method="M-Pesa",
    reference_number="PAY001"
)

print("\nPayment of KSh 3,000:")
print(f"Interest paid: KSh {result['interest_paid']:,.2f}")
print(f"Principal paid: KSh {result['principal_paid']:,.2f}")
print(
    f"Remaining principal: "
    f"KSh {result['remaining_principal']:,.2f}"
)


# 6. Push forward
push_result = push_forward(loan_id)

print("\nPush Forward:")
print(
    f"Principal carried: "
    f"KSh {push_result['principal_carried']:,.2f}"
)

print(
    f"New monthly interest: "
    f"KSh {push_result['new_monthly_interest']:,.2f}"
)

print("\n=== TEST COMPLETE ===")