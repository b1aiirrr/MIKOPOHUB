import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_connection


class PaymentView:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("MikopoHub - Payments")
        self.window.geometry("1250x750")
        self.window.minsize(1050, 650)

        self.selected_loan = None
        self.current_period = None
        self.selected_payment_id = None
        self.loan_records = []

        self.build_interface()
        self.load_loans()

    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def build_interface(self):

        # -----------------------------
        # HEADER
        # -----------------------------

        header = tk.Frame(self.window)
        header.pack(fill="x", padx=25, pady=20)

        tk.Button(
            header,
            text="⬅ Back to Dashboard",
            font=("Arial", 10, "bold"),
            command=self.go_back
        ).pack(side="left", padx=(0, 20))

        tk.Label(
            header,
            text="Payments",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        # -----------------------------
        # LOAN SELECTION
        # -----------------------------

        selection_frame = tk.LabelFrame(
            self.window,
            text="Select Loan",
            padx=15,
            pady=15
        )

        selection_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            selection_frame,
            text="Loan:"
        ).pack(side="left")

        self.loan_combo = ttk.Combobox(
            selection_frame,
            state="readonly",
            width=65
        )

        self.loan_combo.pack(
            side="left",
            padx=10
        )

        self.loan_combo.bind(
            "<<ComboboxSelected>>",
            self.loan_selected
        )

        tk.Button(
            selection_frame,
            text="🔄 Refresh",
            command=self.load_loans
        ).pack(side="left", padx=5)

        # -----------------------------
        # LOAN SUMMARY
        # -----------------------------

        summary_frame = tk.LabelFrame(
            self.window,
            text="Current Loan / Monthly Period",
            padx=15,
            pady=15
        )

        summary_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.borrower_label = self.create_summary_label(
            summary_frame,
            "Borrower"
        )

        self.principal_label = self.create_summary_label(
            summary_frame,
            "Opening Principal"
        )

        self.interest_label = self.create_summary_label(
            summary_frame,
            "Monthly Interest"
        )

        self.interest_paid_label = self.create_summary_label(
            summary_frame,
            "Interest Paid"
        )

        self.interest_remaining_label = self.create_summary_label(
            summary_frame,
            "Interest Remaining"
        )

        self.principal_paid_label = self.create_summary_label(
            summary_frame,
            "Principal Paid"
        )

        self.remaining_principal_label = self.create_summary_label(
            summary_frame,
            "Remaining Principal"
        )

        self.due_date_label = self.create_summary_label(
            summary_frame,
            "Due Date"
        )

        # -----------------------------
        # PAYMENT FORM
        # -----------------------------

        payment_frame = tk.LabelFrame(
            self.window,
            text="Record / Edit Payment",
            padx=15,
            pady=15
        )

        payment_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # Amount

        tk.Label(
            payment_frame,
            text="Payment Amount"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.amount_entry = tk.Entry(
            payment_frame,
            width=20
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Payment method

        tk.Label(
            payment_frame,
            text="Payment Method"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.method_combo = ttk.Combobox(
            payment_frame,
            state="readonly",
            values=[
                "M-Pesa",
                "Cash",
                "Bank",
                "Other"
            ],
            width=18
        )

        self.method_combo.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        self.method_combo.set("M-Pesa")

        # Reference

        tk.Label(
            payment_frame,
            text="Reference Number"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.reference_entry = tk.Entry(
            payment_frame,
            width=20
        )

        self.reference_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Date

        tk.Label(
            payment_frame,
            text="Payment Date"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.date_entry = tk.Entry(
            payment_frame,
            width=20
        )

        self.date_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Record button

        tk.Button(
            payment_frame,
            text="💳 RECORD PAYMENT",
            font=("Arial", 10, "bold"),
            command=self.record_payment
        ).grid(
            row=0,
            column=4,
            rowspan=2,
            padx=15
        )

        # Edit button

        tk.Button(
            payment_frame,
            text="✏️ EDIT PAYMENT",
            font=("Arial", 10, "bold"),
            command=self.edit_payment
        ).grid(
            row=0,
            column=5,
            rowspan=2,
            padx=10
        )

        # Delete button

        tk.Button(
            payment_frame,
            text="🗑️ DELETE PAYMENT",
            font=("Arial", 10, "bold"),
            command=self.delete_payment
        ).grid(
            row=0,
            column=6,
            rowspan=2,
            padx=10
        )

        # -----------------------------
        # PAYMENT HISTORY
        # -----------------------------

        history_frame = tk.LabelFrame(
            self.window,
            text="Payment History",
            padx=10,
            pady=10
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        columns = (
            "id",
            "payment_date",
            "amount",
            "interest",
            "principal",
            "method",
            "reference"
        )

        self.payment_table = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "payment_date": "Date",
            "amount": "Amount",
            "interest": "Interest",
            "principal": "Principal",
            "method": "Method",
            "reference": "Reference"
        }

        for column, heading in headings.items():

            self.payment_table.heading(
                column,
                text=heading
            )

        self.payment_table.column(
            "id",
            width=60
        )

        self.payment_table.column(
            "payment_date",
            width=120
        )

        self.payment_table.column(
            "amount",
            width=130
        )

        self.payment_table.column(
            "interest",
            width=130
        )

        self.payment_table.column(
            "principal",
            width=130
        )

        self.payment_table.column(
            "method",
            width=120
        )

        self.payment_table.column(
            "reference",
            width=180
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.payment_table.yview
        )

        self.payment_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.payment_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.payment_table.bind(
            "<<TreeviewSelect>>",
            self.payment_selected
        )

    # ==================================================
    # SUMMARY LABEL
    # ==================================================

    def create_summary_label(self, parent, title):

        frame = tk.Frame(parent)

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 9)
        ).pack()

        label = tk.Label(
            frame,
            text="KSh 0.00",
            font=("Arial", 11, "bold")
        )

        label.pack(pady=5)

        return label

    # ==================================================
    # BACK
    # ==================================================

    def go_back(self):

        self.window.destroy()

    # ==================================================
    # LOAD LOANS
    # ==================================================

    def load_loans(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                loans.id,
                loans.loan_number,
                loans.principal,
                loans.issue_date,
                loans.status,
                borrowers.full_name

            FROM loans

            INNER JOIN borrowers
                ON borrowers.id = loans.borrower_id

            WHERE loans.status = 'ACTIVE'

            ORDER BY loans.id DESC
            """
        )

        loans = cursor.fetchall()

        connection.close()

        self.loan_records = loans

        loan_values = []

        for loan in loans:

            loan_values.append(
                f"{loan['loan_number']} | "
                f"{loan['full_name']} | "
                f"KSh {loan['principal']:,.2f}"
            )

        self.loan_combo["values"] = loan_values

        if not loan_values:

            self.loan_combo.set(
                "No active loans"
            )

            self.clear_summary()

            return

        self.loan_combo.current(0)

        self.loan_selected()

    # ==================================================
    # LOAN SELECTED
    # ==================================================

    def loan_selected(self, event=None):

        index = self.loan_combo.current()

        if index < 0:
            return

        if index >= len(self.loan_records):
            return

        self.selected_loan = self.loan_records[index]

        self.selected_payment_id = None

        self.load_current_period()

    # ==================================================
    # LOAD CURRENT PERIOD
    # ==================================================

    def load_current_period(self):

        if not self.selected_loan:
            return

        loan_id = self.selected_loan["id"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                monthly_periods.*,
                loans.principal AS loan_principal,
                borrowers.full_name

            FROM monthly_periods

            INNER JOIN loans
                ON loans.id = monthly_periods.loan_id

            INNER JOIN borrowers
                ON borrowers.id = loans.borrower_id

            WHERE monthly_periods.loan_id = ?

            AND monthly_periods.status = 'ACTIVE'

            ORDER BY monthly_periods.id DESC

            LIMIT 1
            """,
            (loan_id,)
        )

        period = cursor.fetchone()

        connection.close()

        if period is None:

            self.current_period = None

            self.clear_summary()

            self.load_payment_history()

            return

        self.current_period = period

        self.update_summary()

        self.load_payment_history()

    # ==================================================
    # UPDATE SUMMARY
    # ==================================================

    def update_summary(self):

        if not self.current_period:
            return

        period = self.current_period

        opening_principal = period["opening_principal"]
        interest_due = period["interest_due"]
        interest_paid = period["interest_paid"]
        principal_paid = period["principal_paid"]

        interest_remaining = max(
            0,
            interest_due - interest_paid
        )

        remaining_principal = max(
            0,
            opening_principal - principal_paid
        )

        self.borrower_label.config(
            text=period["full_name"]
        )

        self.principal_label.config(
            text=f"KSh {opening_principal:,.2f}"
        )

        self.interest_label.config(
            text=f"KSh {interest_due:,.2f}"
        )

        self.interest_paid_label.config(
            text=f"KSh {interest_paid:,.2f}"
        )

        self.interest_remaining_label.config(
            text=f"KSh {interest_remaining:,.2f}"
        )

        self.principal_paid_label.config(
            text=f"KSh {principal_paid:,.2f}"
        )

        self.remaining_principal_label.config(
            text=f"KSh {remaining_principal:,.2f}"
        )

        self.due_date_label.config(
            text=period["month_end"]
        )

    # ==================================================
    # RECORD PAYMENT
    # ==================================================

    def record_payment(self):

        if not self.selected_loan:

            messagebox.showwarning(
                "No Loan",
                "Please select a loan first."
            )

            return

        if not self.current_period:

            messagebox.showwarning(
                "No Active Period",
                "This loan does not have an active monthly period."
            )

            return

        payment_data = self.get_form_data()

        if payment_data is None:
            return

        amount, payment_date, payment_method, reference = payment_data

        connection = get_connection()
        cursor = connection.cursor()

        try:

            interest_portion, principal_portion = (
                self.calculate_allocation(
                    amount,
                    self.current_period
                )
            )

            total_outstanding = (
                max(
                    0,
                    self.current_period["interest_due"]
                    - self.current_period["interest_paid"]
                )
                +
                max(
                    0,
                    self.current_period["opening_principal"]
                    - self.current_period["principal_paid"]
                )
            )

            if amount > total_outstanding:

                connection.close()

                messagebox.showwarning(
                    "Payment Too Large",
                    f"Maximum outstanding amount is:\n\n"
                    f"KSh {total_outstanding:,.2f}"
                )

                return

            confirmed = messagebox.askyesno(
                "Confirm Payment",
                f"Amount: KSh {amount:,.2f}\n\n"
                f"Interest: KSh {interest_portion:,.2f}\n"
                f"Principal: KSh {principal_portion:,.2f}\n\n"
                f"Date: {payment_date}\n"
                f"Method: {payment_method}\n\n"
                "Record this payment?"
            )

            if not confirmed:

                connection.close()

                return

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
                    self.selected_loan["id"],
                    self.current_period["id"],
                    payment_date,
                    amount,
                    interest_portion,
                    principal_portion,
                    payment_method,
                    reference
                )
            )

            connection.commit()

            connection.close()

            self.recalculate_period()

            self.clear_payment_form()

            # Check whether loan has now been completed

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT status
                FROM loans
                WHERE id = ?
                """,
                (self.selected_loan["id"],)
            )

            loan_status = cursor.fetchone()

            connection.close()

            if (
                loan_status
                and loan_status["status"] == "COMPLETED"
            ):

                messagebox.showinfo(
                    "Loan Completed",
                    "Payment has been recorded successfully.\n\n"
                    "Congratulations! The loan has been fully paid "
                    "and is now marked as COMPLETED."
                )

                self.selected_loan = None
                self.current_period = None

                self.load_loans()

                return

            messagebox.showinfo(
                "Payment Recorded",
                "Payment has been recorded successfully."
            )

            self.load_current_period()

        except Exception as error:

            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Error",
                f"Could not record payment.\n\n{error}"
            )

    # ==================================================
    # PAYMENT SELECTED
    # ==================================================

    def payment_selected(self, event=None):

        selected = self.payment_table.selection()

        if not selected:
            return

        item = self.payment_table.item(
            selected[0]
        )

        values = item["values"]

        if not values:
            return

        self.selected_payment_id = int(
            values[0]
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.insert(
            0,
            str(values[2]).replace(
                "KSh ",
                ""
            ).replace(
                ",",
                ""
            )
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            values[1]
        )

        self.method_combo.set(
            values[5]
        )

        self.reference_entry.delete(
            0,
            tk.END
        )

        self.reference_entry.insert(
            0,
            values[6]
        )

    # ==================================================
    # EDIT PAYMENT
    # ==================================================

    def edit_payment(self):

        if not self.selected_payment_id:

            messagebox.showwarning(
                "Select Payment",
                "Please select a payment from the payment history first."
            )

            return

        payment_data = self.get_form_data()

        if payment_data is None:
            return

        amount, payment_date, payment_method, reference = payment_data

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # Get original payment

            cursor.execute(
                """
                SELECT *
                FROM payments
                WHERE id = ?
                """,
                (self.selected_payment_id,)
            )

            old_payment = cursor.fetchone()

            if old_payment is None:

                connection.close()

                messagebox.showerror(
                    "Not Found",
                    "The selected payment no longer exists."
                )

                return

            # Make sure payment belongs to selected loan

            if old_payment["loan_id"] != self.selected_loan["id"]:

                connection.close()

                messagebox.showerror(
                    "Invalid Payment",
                    "The selected payment does not belong to this loan."
                )

                return

            confirmed = messagebox.askyesno(
                "Confirm Edit",
                f"New Amount: KSh {amount:,.2f}\n\n"
                f"Date: {payment_date}\n"
                f"Method: {payment_method}\n"
                f"Reference: {reference}\n\n"
                "Update this payment?"
            )

            if not confirmed:

                connection.close()

                return

            cursor.execute(
                """
                UPDATE payments

                SET
                    payment_date = ?,
                    amount = ?,
                    payment_method = ?,
                    reference_number = ?

                WHERE id = ?
                """,
                (
                    payment_date,
                    amount,
                    payment_method,
                    reference,
                    self.selected_payment_id
                )
            )

            connection.commit()

            connection.close()

            # Recalculate every payment for the period

            self.recalculate_period()

            messagebox.showinfo(
                "Payment Updated",
                "Payment has been updated successfully."
            )

            self.selected_payment_id = None

            self.clear_payment_form()

            self.load_current_period()

        except Exception as error:

            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Edit Error",
                f"Could not update payment.\n\n{error}"
            )

    # ==================================================
    # DELETE PAYMENT
    # ==================================================

    def delete_payment(self):

        if not self.selected_payment_id:

            messagebox.showwarning(
                "Select Payment",
                "Please select a payment from the payment history first."
            )

            return

        confirmed = messagebox.askyesno(
            "Delete Payment",
            "Are you sure you want to delete this payment?\n\n"
            "This action will recalculate the monthly loan balances."
        )

        if not confirmed:
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT *
                FROM payments
                WHERE id = ?
                """,
                (self.selected_payment_id,)
            )

            payment = cursor.fetchone()

            if payment is None:

                connection.close()

                messagebox.showerror(
                    "Not Found",
                    "The selected payment no longer exists."
                )

                return

            if payment["loan_id"] != self.selected_loan["id"]:

                connection.close()

                messagebox.showerror(
                    "Invalid Payment",
                    "This payment does not belong to the selected loan."
                )

                return

            cursor.execute(
                """
                DELETE FROM payments
                WHERE id = ?
                """,
                (self.selected_payment_id,)
            )

            connection.commit()

            connection.close()

            self.selected_payment_id = None

            self.clear_payment_form()

            # Recalculate balances

            self.recalculate_period()

            messagebox.showinfo(
                "Payment Deleted",
                "Payment has been deleted successfully."
            )

            self.load_current_period()

        except Exception as error:

            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Delete Error",
                f"Could not delete payment.\n\n{error}"
            )

    # ==================================================
    # GET FORM DATA
    # ==================================================

    def get_form_data(self):

        try:

            amount = float(
                self.amount_entry.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid payment amount."
            )

            return None

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Payment amount must be greater than zero."
            )

            return None

        payment_date = (
            self.date_entry.get().strip()
        )

        try:

            datetime.strptime(
                payment_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Date must use YYYY-MM-DD."
            )

            return None

        payment_method = (
            self.method_combo.get().strip()
        )

        if not payment_method:

            messagebox.showerror(
                "Payment Method",
                "Please select a payment method."
            )

            return None

        reference = (
            self.reference_entry.get().strip()
        )

        return (
            amount,
            payment_date,
            payment_method,
            reference
        )

    # ==================================================
    # CALCULATE PAYMENT ALLOCATION
    # ==================================================

    def calculate_allocation(
        self,
        amount,
        period
    ):

        outstanding_interest = max(
            0,
            period["interest_due"]
            - period["interest_paid"]
        )

        outstanding_principal = max(
            0,
            period["opening_principal"]
            - period["principal_paid"]
        )

        interest_portion = min(
            amount,
            outstanding_interest
        )

        remaining = (
            amount
            - interest_portion
        )

        principal_portion = min(
            remaining,
            outstanding_principal
        )

        return (
            interest_portion,
            principal_portion
        )

    # ==================================================
    # RECALCULATE PERIOD
    # ==================================================

    def recalculate_period(self):

        if not self.current_period:
            return

        period_id = self.current_period["id"]
        loan_id = self.current_period["loan_id"]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # ------------------------------------------
            # Get period
            # ------------------------------------------

            cursor.execute(
                """
                SELECT *
                FROM monthly_periods
                WHERE id = ?
                """,
                (period_id,)
            )

            period = cursor.fetchone()

            if period is None:

                connection.close()

                return

            # ------------------------------------------
            # Get all payments for this period
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    id,
                    amount

                FROM payments

                WHERE monthly_period_id = ?

                ORDER BY payment_date ASC, id ASC
                """,
                (period_id,)
            )

            payments = cursor.fetchall()

            total_interest_paid = 0.0
            total_principal_paid = 0.0

            remaining_interest = (
                period["interest_due"]
            )

            remaining_principal = (
                period["opening_principal"]
            )

            # ------------------------------------------
            # Recalculate every payment
            # ------------------------------------------

            for payment in payments:

                amount = payment["amount"]

                interest_portion = min(
                    amount,
                    max(
                        0,
                        remaining_interest
                    )
                )

                remaining_after_interest = (
                    amount
                    - interest_portion
                )

                principal_portion = min(
                    remaining_after_interest,
                    max(
                        0,
                        remaining_principal
                    )
                )

                remaining_interest -= (
                    interest_portion
                )

                remaining_principal -= (
                    principal_portion
                )

                total_interest_paid += (
                    interest_portion
                )

                total_principal_paid += (
                    principal_portion
                )

                cursor.execute(
                    """
                    UPDATE payments

                    SET
                        interest_portion = ?,
                        principal_portion = ?

                    WHERE id = ?
                    """,
                    (
                        interest_portion,
                        principal_portion,
                        payment["id"]
                    )
                )

            # ------------------------------------------
            # Determine period status
            # ------------------------------------------

            if (
                remaining_interest <= 0.000001
                and remaining_principal <= 0.000001
            ):

                status = "COMPLETED"

            else:

                status = "ACTIVE"

            # ------------------------------------------
            # Update monthly period
            # ------------------------------------------

            cursor.execute(
                """
                UPDATE monthly_periods

                SET
                    interest_paid = ?,
                    principal_paid = ?,
                    status = ?

                WHERE id = ?
                """,
                (
                    total_interest_paid,
                    total_principal_paid,
                    status,
                    period_id
                )
            )

            # ------------------------------------------
            # UPDATE ACTUAL LOAN STATUS
            # ------------------------------------------

            if status == "COMPLETED":

                cursor.execute(
                    """
                    UPDATE loans

                    SET
                        status = 'COMPLETED'

                    WHERE id = ?
                    """,
                    (loan_id,)
                )

            else:

                cursor.execute(
                    """
                    UPDATE loans

                    SET
                        status = 'ACTIVE'

                    WHERE id = ?
                    """,
                    (loan_id,)
                )

            connection.commit()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Recalculation Error",
                f"Could not recalculate the loan period.\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # LOAD PAYMENT HISTORY
    # ==================================================

    def load_payment_history(self):

        for row in self.payment_table.get_children():

            self.payment_table.delete(row)

        if not self.selected_loan:
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                payment_date,
                amount,
                interest_portion,
                principal_portion,
                payment_method,
                reference_number

            FROM payments

            WHERE loan_id = ?

            ORDER BY payment_date DESC, id DESC
            """,
            (self.selected_loan["id"],)
        )

        payments = cursor.fetchall()

        connection.close()

        for payment in payments:

            self.payment_table.insert(
                "",
                "end",
                values=(
                    payment["id"],
                    payment["payment_date"],
                    f"KSh {payment['amount']:,.2f}",
                    f"KSh {payment['interest_portion']:,.2f}",
                    f"KSh {payment['principal_portion']:,.2f}",
                    payment["payment_method"] or "",
                    payment["reference_number"] or ""
                )
            )

    # ==================================================
    # CLEAR PAYMENT FORM
    # ==================================================

    def clear_payment_form(self):

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.reference_entry.delete(
            0,
            tk.END
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.method_combo.set(
            "M-Pesa"
        )

        self.selected_payment_id = None

    # ==================================================
    # CLEAR SUMMARY
    # ==================================================

    def clear_summary(self):

        labels = [
            self.borrower_label,
            self.principal_label,
            self.interest_label,
            self.interest_paid_label,
            self.interest_remaining_label,
            self.principal_paid_label,
            self.remaining_principal_label,
            self.due_date_label
        ]

        for label in labels:

            label.config(
                text="KSh 0.00"
            )

        for row in self.payment_table.get_children():

            self.payment_table.delete(row)


# ======================================================
# DIRECT TEST
# ======================================================

if __name__ == "__main__":

    from database import initialize_database

    initialize_database()

    root = tk.Tk()
    root.withdraw()

    PaymentView(root)

    root.mainloop()