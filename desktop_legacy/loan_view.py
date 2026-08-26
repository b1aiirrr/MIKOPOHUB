import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import calendar

from database import get_connection


INTEREST_RATE = 20.0


# ======================================================
# DATE UTILITIES
# ======================================================

def add_one_month(original_date):
    """
    Add one calendar month while handling dates such as
    31 January correctly.
    """

    year = original_date.year
    month = original_date.month

    if month == 12:
        new_year = year + 1
        new_month = 1
    else:
        new_year = year
        new_month = month + 1

    last_day = calendar.monthrange(
        new_year,
        new_month
    )[1]

    new_day = min(
        original_date.day,
        last_day
    )

    return date(
        new_year,
        new_month,
        new_day
    )


def calculate_days_remaining(due_date_text):
    """
    Calculate the number of days remaining until the due date.
    """

    if not due_date_text:
        return None

    try:
        due_date = date.fromisoformat(
            due_date_text
        )

    except ValueError:
        return None

    return (
        due_date - date.today()
    ).days


def get_display_status(status, days_remaining):
    """
    Determine the status displayed to the user.

    Database status is preserved unless the loan is ACTIVE.
    """

    if status == "VOID":
        return "VOID"

    if status == "PAID":
        return "PAID"

    if status == "DEFAULTED":
        return "DEFAULTED"

    if status == "PUSHED FORWARD":
        return "PUSHED FORWARD"

    if status == "ACTIVE":

        if days_remaining is None:
            return "ACTIVE"

        if days_remaining < 0:
            return "OVERDUE"

        if days_remaining == 0:
            return "DUE TODAY"

        return "ACTIVE"

    return status


def format_days(days_remaining):
    """
    Make the Days column easier to understand.
    """

    if days_remaining is None:
        return "-"

    if days_remaining < 0:

        overdue_days = abs(
            days_remaining
        )

        if overdue_days == 1:
            return "1 day overdue"

        return (
            f"{overdue_days} days overdue"
        )

    if days_remaining == 0:
        return "DUE TODAY"

    if days_remaining == 1:
        return "1 day"

    return f"{days_remaining} days"


# ======================================================
# LOAN VIEW
# ======================================================

class LoanView:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "MikopoHub - Loans"
        )

        self.window.geometry(
            "1350x750"
        )

        self.window.minsize(
            1100,
            600
        )

        self.build_interface()

    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def build_interface(self):

        # ----------------------------------------------
        # HEADER
        # ----------------------------------------------

        header = tk.Frame(
            self.window
        )

        header.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Button(
            header,
            text="⬅ Back to Dashboard",
            font=("Arial", 10, "bold"),
            command=self.go_back
        ).pack(
            side="left",
            padx=(0, 20)
        )

        tk.Label(
            header,
            text="Loans",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Button(
            header,
            text="+ Create New Loan",
            font=("Arial", 11, "bold"),
            command=self.open_create_loan
        ).pack(
            side="right"
        )

        # ----------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------

        actions = tk.Frame(
            self.window
        )

        actions.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Button(
            actions,
            text="✏️ Edit Selected",
            command=self.edit_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            actions,
            text="👁️ Borrower History",
            command=self.show_borrower_history
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            actions,
            text="🗑️ Delete / Void",
            command=self.delete_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            actions,
            text="🔄 Refresh",
            command=self.load_loans
        ).pack(
            side="left",
            padx=5
        )

        tk.Label(
            actions,
            text=(
                "Loan dates are tracked automatically "
                "from the borrowing date."
            ),
            font=("Arial", 9)
        ).pack(
            side="right",
            padx=10
        )

        # ----------------------------------------------
        # SEARCH
        # ----------------------------------------------

        search_frame = tk.Frame(
            self.window
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=(10, 5)
        )

        tk.Label(
            search_frame,
            text="🔍 Search Loans:",
            font=("Arial", 10, "bold")
        ).pack(
            side="left"
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=45,
            font=("Arial", 10)
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_loans()
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.load_loans
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search
        ).pack(
            side="left",
            padx=3
        )

        tk.Label(
            search_frame,
            text=(
                "Search by Loan No., borrower name, "
                "phone or National ID"
            ),
            font=("Arial", 9)
        ).pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------
        # TABLE
        # ----------------------------------------------

        table_frame = tk.Frame(
            self.window
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        columns = (
            "loan_number",
            "borrower",
            "principal",
            "interest",
            "issue_date",
            "due_date",
            "days",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "loan_number": "Loan No.",
            "borrower": "Borrower",
            "principal": "Principal",
            "interest": "Monthly Interest",
            "issue_date": "Date Borrowed",
            "due_date": "Due Date",
            "days": "Time Remaining",
            "status": "Status"
        }

        for column, heading in headings.items():

            self.table.heading(
                column,
                text=heading
            )

        widths = {
            "loan_number": 100,
            "borrower": 210,
            "principal": 130,
            "interest": 140,
            "issue_date": 120,
            "due_date": 120,
            "days": 140,
            "status": 140
        }

        for column, width in widths.items():

            self.table.column(
                column,
                width=width,
                anchor="center"
            )

        self.table.column(
            "borrower",
            anchor="w"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # DOUBLE CLICK TO EDIT
        self.table.bind(
            "<Double-1>",
            lambda event: self.edit_selected()
        )

        # ----------------------------------------------
        # STATUS BAR
        # ----------------------------------------------

        self.result_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 9)
        )

        self.result_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        self.load_loans()

    # ==================================================
    # BACK TO DASHBOARD
    # ==================================================

    def go_back(self):

        self.window.destroy()

    # ==================================================
    # CLEAR SEARCH
    # ==================================================

    def clear_search(self):

        self.search_var.set("")

        self.load_loans()

        self.search_entry.focus_set()

    # ==================================================
    # LOAD LOANS
    # ==================================================

    def load_loans(self):

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            search = ""

            if hasattr(
                self,
                "search_var"
            ):
                search = (
                    self.search_var
                    .get()
                    .strip()
                )

            query = """
                SELECT
                    loans.id,
                    loans.loan_number,
                    loans.borrower_id,
                    borrowers.full_name,
                    borrowers.phone,
                    borrowers.national_id,
                    loans.principal,
                    loans.interest_rate,
                    loans.issue_date,
                    loans.due_date,
                    loans.status

                FROM loans

                JOIN borrowers
                    ON loans.borrower_id = borrowers.id
            """

            params = []

            # ------------------------------------------
            # SEARCH FILTER
            # ------------------------------------------

            if search:

                query += """
                    WHERE
                        loans.loan_number LIKE ?
                        OR borrowers.full_name LIKE ?
                        OR borrowers.phone LIKE ?
                        OR borrowers.national_id LIKE ?
                """

                term = f"%{search}%"

                params = [
                    term,
                    term,
                    term,
                    term
                ]

            query += """
                ORDER BY loans.id DESC
            """

            cursor.execute(
                query,
                params
            )

            loans = cursor.fetchall()

            # ------------------------------------------
            # CLEAR TABLE
            # ------------------------------------------

            for row in self.table.get_children():

                self.table.delete(
                    row
                )

            # ------------------------------------------
            # INSERT LOANS
            # ------------------------------------------

            for loan in loans:

                days_remaining = (
                    calculate_days_remaining(
                        loan["due_date"]
                    )
                )

                monthly_interest = (
                    loan["principal"]
                    * loan["interest_rate"]
                    / 100
                )

                display_status = (
                    get_display_status(
                        loan["status"],
                        days_remaining
                    )
                )

                formatted_days = (
                    format_days(
                        days_remaining
                    )
                )

                self.table.insert(
                    "",
                    "end",
                    iid=str(
                        loan["id"]
                    ),
                    values=(
                        loan["loan_number"],
                        loan["full_name"],
                        f"KSh {loan['principal']:,.2f}",
                        f"KSh {monthly_interest:,.2f}",
                        loan["issue_date"],
                        loan["due_date"],
                        formatted_days,
                        display_status
                    )
                )

            # ------------------------------------------
            # RESULT COUNT
            # ------------------------------------------

            if search:

                self.result_label.config(
                    text=(
                        f"Search results: "
                        f"{len(loans)} loan(s) found "
                        f"for '{search}'"
                    )
                )

            else:

                self.result_label.config(
                    text=(
                        f"Total loans displayed: "
                        f"{len(loans)}"
                    )
                )

        except Exception as error:

            print(
                "Loan loading error:",
                error
            )

            messagebox.showerror(
                "Database Error",
                f"Unable to load loans.\n\n{error}"
            )

        finally:

            if connection:

                connection.close()

    # ==================================================
    # GET SELECTED LOAN
    # ==================================================

    def get_selected_id(self):

        selected = (
            self.table.selection()
        )

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a loan first."
            )

            return None

        return int(
            selected[0]
        )

    # ==================================================
    # CREATE LOAN
    # ==================================================

    def open_create_loan(self):

        CreateLoanWindow(
            self.window,
            self.load_loans
        )

    # ==================================================
    # EDIT LOAN
    # ==================================================

    def edit_selected(self):

        loan_id = (
            self.get_selected_id()
        )

        if loan_id is None:
            return

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

        connection.close()

        if loan is None:

            messagebox.showerror(
                "Error",
                "Loan could not be found."
            )

            return

        EditLoanWindow(
            self.window,
            loan,
            self.load_loans
        )

    # ==================================================
    # BORROWER HISTORY
    # ==================================================

    def show_borrower_history(self):

        loan_id = (
            self.get_selected_id()
        )

        if loan_id is None:
            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ------------------------------------------
            # GET BORROWER
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    borrowers.id,
                    borrowers.borrower_number,
                    borrowers.full_name,
                    borrowers.phone,
                    borrowers.national_id,
                    borrowers.location

                FROM loans

                JOIN borrowers
                    ON loans.borrower_id = borrowers.id

                WHERE loans.id = ?
                """,
                (loan_id,)
            )

            borrower = cursor.fetchone()

            if borrower is None:

                messagebox.showerror(
                    "Error",
                    "Borrower could not be found."
                )

                return

            borrower_id = (
                borrower["id"]
            )

            # ------------------------------------------
            # GET ALL LOANS
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    loans.id,
                    loans.loan_number,
                    loans.principal,
                    loans.interest_rate,
                    loans.issue_date,
                    loans.due_date,
                    loans.status

                FROM loans

                WHERE borrower_id = ?

                ORDER BY loans.id DESC
                """,
                (borrower_id,)
            )

            loans = cursor.fetchall()

            # ------------------------------------------
            # GET PAYMENT TOTALS PER LOAN
            # ------------------------------------------

            loan_data = []

            total_lent = 0
            total_principal_paid = 0
            total_interest_paid = 0

            for loan in loans:

                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            SUM(principal_portion),
                            0
                        ) AS principal_paid,

                        COALESCE(
                            SUM(interest_portion),
                            0
                        ) AS interest_paid

                    FROM payments

                    WHERE loan_id = ?
                    """,
                    (loan["id"],)
                )

                payment = (
                    cursor.fetchone()
                )

                principal_paid = (
                    payment["principal_paid"]
                    or 0
                )

                interest_paid = (
                    payment["interest_paid"]
                    or 0
                )

                remaining = max(
                    0,
                    loan["principal"]
                    - principal_paid
                )

                total_lent += (
                    loan["principal"]
                )

                total_principal_paid += (
                    principal_paid
                )

                total_interest_paid += (
                    interest_paid
                )

                loan_data.append(
                    {
                        "loan_number":
                            loan["loan_number"],

                        "principal":
                            loan["principal"],

                        "principal_paid":
                            principal_paid,

                        "remaining":
                            remaining,

                        "interest_paid":
                            interest_paid,

                        "issue_date":
                            loan["issue_date"],

                        "due_date":
                            loan["due_date"],

                        "status":
                            loan["status"]
                    }
                )

            # ------------------------------------------
            # TOTAL REMAINING
            # ------------------------------------------

            total_remaining = max(
                0,
                total_lent
                - total_principal_paid
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load borrower history.\n\n{error}"
            )

            return

        finally:

            if connection:

                connection.close()

        # ----------------------------------------------
        # HISTORY WINDOW
        # ----------------------------------------------

        HistoryWindow(
            self.window,
            borrower,
            loan_data,
            total_lent,
            total_principal_paid,
            total_remaining,
            total_interest_paid
        )

    # ==================================================
    # DELETE / VOID LOAN
    # ==================================================

    def delete_selected(self):

        loan_id = (
            self.get_selected_id()
        )

        if loan_id is None:
            return

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                loans.loan_number,
                loans.status,
                borrowers.full_name

            FROM loans

            JOIN borrowers
                ON loans.borrower_id = borrowers.id

            WHERE loans.id = ?
            """,
            (loan_id,)
        )

        loan = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM payments
            WHERE loan_id = ?
            """,
            (loan_id,)
        )

        payment_count = (
            cursor.fetchone()["total"]
        )

        connection.close()

        if loan is None:
            return

        # ------------------------------------------
        # PROTECT LOANS WITH PAYMENT HISTORY
        # ------------------------------------------

        if payment_count > 0:

            messagebox.showwarning(
                "Loan Protected",
                f"{loan['loan_number']} already has "
                "payment history.\n\n"
                "It cannot be permanently deleted.\n\n"
                "Use Edit to change the status."
            )

            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete this loan?\n\n"
            f"Loan: {loan['loan_number']}\n"
            f"Borrower: {loan['full_name']}\n\n"
            "This loan has no payments."
        )

        if not confirmed:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM loans
                WHERE id = ?
                """,
                (loan_id,)
            )

            connection.commit()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Delete Error",
                f"Loan could not be deleted.\n\n{error}"
            )

            connection.close()

            return

        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Loan deleted successfully."
        )

        self.load_loans()


# ======================================================
# BORROWER HISTORY WINDOW
# ======================================================

class HistoryWindow:

    def __init__(
        self,
        parent,
        borrower,
        loan_data,
        total_lent,
        total_principal_paid,
        total_remaining,
        total_interest_paid
    ):

        self.borrower = borrower
        self.loan_data = loan_data

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "MikopoHub - Borrower Loan History"
        )

        self.window.geometry(
            "1200x700"
        )

        self.window.minsize(
            950,
            600
        )

        self.build_interface(
            total_lent,
            total_principal_paid,
            total_remaining,
            total_interest_paid
        )

    # ==================================================
    # BUILD HISTORY INTERFACE
    # ==================================================

    def build_interface(
        self,
        total_lent,
        total_principal_paid,
        total_remaining,
        total_interest_paid
    ):

        # ----------------------------------------------
        # HEADER
        # ----------------------------------------------

        header = tk.Frame(
            self.window
        )

        header.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Label(
            header,
            text="Borrower Loan History",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Button(
            header,
            text="Close",
            command=self.window.destroy
        ).pack(
            side="right"
        )

        # ----------------------------------------------
        # BORROWER INFORMATION
        # ----------------------------------------------

        borrower_frame = tk.Frame(
            self.window,
            relief="solid",
            borderwidth=1,
            padx=20,
            pady=15
        )

        borrower_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            borrower_frame,
            text=(
                f"Borrower: "
                f"{self.borrower['full_name']}"
            ),
            font=("Arial", 15, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            borrower_frame,
            text=(
                f"Borrower No: "
                f"{self.borrower['borrower_number']}"
            )
        ).pack(
            anchor="w",
            pady=2
        )

        tk.Label(
            borrower_frame,
            text=(
                f"Phone: "
                f"{self.borrower['phone']}"
            )
        ).pack(
            anchor="w",
            pady=2
        )

        if self.borrower["national_id"]:

            tk.Label(
                borrower_frame,
                text=(
                    f"National ID: "
                    f"{self.borrower['national_id']}"
                )
            ).pack(
                anchor="w",
                pady=2
            )

        # ----------------------------------------------
        # SUMMARY CARDS
        # ----------------------------------------------

        summary = tk.Frame(
            self.window
        )

        summary.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.create_summary_card(
            summary,
            "💰 Total Principal Lent",
            total_lent
        )

        self.create_summary_card(
            summary,
            "💵 Principal Returned",
            total_principal_paid
        )

        self.create_summary_card(
            summary,
            "📌 Principal Remaining",
            total_remaining
        )

        self.create_summary_card(
            summary,
            "📈 Interest Collected",
            total_interest_paid
        )

        # ----------------------------------------------
        # LOAN HISTORY TITLE
        # ----------------------------------------------

        tk.Label(
            self.window,
            text="Complete Loan History",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 5)
        )

        # ----------------------------------------------
        # LOAN TABLE
        # ----------------------------------------------

        table_frame = tk.Frame(
            self.window
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 20)
        )

        columns = (
            "loan_number",
            "principal",
            "principal_paid",
            "remaining",
            "interest_paid",
            "issue_date",
            "due_date",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "loan_number": "Loan No.",
            "principal": "Principal",
            "principal_paid": "Principal Returned",
            "remaining": "Principal Remaining",
            "interest_paid": "Interest Paid",
            "issue_date": "Date Borrowed",
            "due_date": "Due Date",
            "status": "Status"
        }

        for column, heading in headings.items():

            self.table.heading(
                column,
                text=heading
            )

        widths = {
            "loan_number": 95,
            "principal": 120,
            "principal_paid": 140,
            "remaining": 145,
            "interest_paid": 120,
            "issue_date": 115,
            "due_date": 115,
            "status": 130
        }

        for column, width in widths.items():

            self.table.column(
                column,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------
        # INSERT HISTORY
        # ----------------------------------------------

        for loan in self.loan_data:

            self.table.insert(
                "",
                "end",
                values=(
                    loan["loan_number"],
                    f"KSh {loan['principal']:,.2f}",
                    f"KSh {loan['principal_paid']:,.2f}",
                    f"KSh {loan['remaining']:,.2f}",
                    f"KSh {loan['interest_paid']:,.2f}",
                    loan["issue_date"],
                    loan["due_date"],
                    loan["status"]
                )
            )

    # ==================================================
    # SUMMARY CARD
    # ==================================================

    def create_summary_card(
        self,
        parent,
        title,
        amount
    ):

        card = tk.Frame(
            parent,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=10
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 9)
        ).pack()

        tk.Label(
            card,
            text=f"KSh {amount:,.2f}",
            font=("Arial", 14, "bold")
        ).pack(
            pady=5
        )


# ======================================================
# CREATE LOAN WINDOW
# ======================================================

class CreateLoanWindow:

    def __init__(
        self,
        parent,
        refresh_callback
    ):

        self.refresh_callback = (
            refresh_callback
        )

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "MikopoHub - Create Loan"
        )

        self.window.geometry(
            "620x760"
        )

        self.window.resizable(
            False,
            False
        )

        self.build_form()

    # ==================================================
    # BUILD FORM
    # ==================================================

    def build_form(self):

        container = tk.Frame(
            self.window,
            padx=30,
            pady=25
        )

        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="Create New Loan",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 20)
        )

        # ----------------------------------------------
        # BORROWER
        # ----------------------------------------------

        tk.Label(
            container,
            text="Borrower"
        ).pack(
            anchor="w"
        )

        self.borrower_var = tk.StringVar()

        self.borrower_combo = ttk.Combobox(
            container,
            textvariable=self.borrower_var,
            state="readonly",
            width=50
        )

        self.borrower_combo.pack(
            fill="x",
            pady=(5, 15)
        )

        self.load_borrowers()

        # ----------------------------------------------
        # PRINCIPAL
        # ----------------------------------------------

        tk.Label(
            container,
            text="Loan Principal (KSh)"
        ).pack(
            anchor="w"
        )

        self.principal_entry = tk.Entry(
            container
        )

        self.principal_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        self.principal_entry.bind(
            "<KeyRelease>",
            self.calculate_values
        )

        # ----------------------------------------------
        # INTEREST
        # ----------------------------------------------

        interest_frame = tk.Frame(
            container
        )

        interest_frame.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            interest_frame,
            text="Interest Rate:"
        ).pack(
            side="left"
        )

        tk.Label(
            interest_frame,
            text="20% per month",
            font=("Arial", 11, "bold")
        ).pack(
            side="right"
        )

        monthly_frame = tk.Frame(
            container
        )

        monthly_frame.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            monthly_frame,
            text="Monthly Interest:"
        ).pack(
            side="left"
        )

        self.interest_label = tk.Label(
            monthly_frame,
            text="KSh 0.00",
            font=("Arial", 11, "bold")
        )

        self.interest_label.pack(
            side="right"
        )

        # ----------------------------------------------
        # DATES
        # ----------------------------------------------

        date_frame = tk.Frame(
            container
        )

        date_frame.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            date_frame,
            text="Date Borrowed:"
        ).pack(
            side="left"
        )

        self.issue_date = date.today()

        self.issue_date_label = tk.Label(
            date_frame,
            text=str(
                self.issue_date
            ),
            font=("Arial", 11, "bold")
        )

        self.issue_date_label.pack(
            side="right"
        )

        due_frame = tk.Frame(
            container
        )

        due_frame.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            due_frame,
            text="First Due Date:"
        ).pack(
            side="left"
        )

        self.due_date = add_one_month(
            self.issue_date
        )

        self.due_date_label = tk.Label(
            due_frame,
            text=str(
                self.due_date
            ),
            font=("Arial", 11, "bold")
        )

        self.due_date_label.pack(
            side="right"
        )

        # ----------------------------------------------
        # FORM FEE
        # ----------------------------------------------

        tk.Label(
            container,
            text="Form Fee",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.form_fee_label = tk.Label(
            container,
            text="Select borrower to check form fee."
        )

        self.form_fee_label.pack(
            anchor="w"
        )

        self.borrower_combo.bind(
            "<<ComboboxSelected>>",
            self.check_form_fee
        )

        # ----------------------------------------------
        # COLLATERAL
        # ----------------------------------------------

        tk.Label(
            container,
            text="Collateral / Security",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        tk.Label(
            container,
            text="Security Type"
        ).pack(
            anchor="w"
        )

        self.security_type_entry = tk.Entry(
            container
        )

        self.security_type_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="Security Description"
        ).pack(
            anchor="w"
        )

        self.description_entry = tk.Entry(
            container
        )

        self.description_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="Estimated Value (KSh)"
        ).pack(
            anchor="w"
        )

        self.collateral_value_entry = tk.Entry(
            container
        )

        self.collateral_value_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="Serial Number (optional)"
        ).pack(
            anchor="w"
        )

        self.serial_entry = tk.Entry(
            container
        )

        self.serial_entry.pack(
            fill="x",
            pady=5
        )

        # ----------------------------------------------
        # CREATE
        # ----------------------------------------------

        tk.Button(
            container,
            text="CREATE LOAN",
            font=("Arial", 11, "bold"),
            command=self.create_loan
        ).pack(
            fill="x",
            pady=25
        )

        self.calculate_values()

    # ==================================================
    # LOAD BORROWERS
    # ==================================================

    def load_borrowers(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                borrower_number,
                full_name

            FROM borrowers

            ORDER BY full_name
            """
        )

        self.borrowers = (
            cursor.fetchall()
        )

        connection.close()

        values = []

        for borrower in self.borrowers:

            values.append(
                f"{borrower['borrower_number']} - "
                f"{borrower['full_name']}"
            )

        self.borrower_combo[
            "values"
        ] = values

    # ==================================================
    # CALCULATE VALUES
    # ==================================================

    def calculate_values(
        self,
        event=None
    ):

        try:

            principal = float(
                self.principal_entry.get()
            )

            monthly_interest = (
                principal
                * INTEREST_RATE
                / 100
            )

            self.interest_label.config(
                text=(
                    f"KSh "
                    f"{monthly_interest:,.2f}"
                )
            )

        except ValueError:

            self.interest_label.config(
                text="KSh 0.00"
            )

        self.issue_date = date.today()

        self.due_date = add_one_month(
            self.issue_date
        )

        self.issue_date_label.config(
            text=str(
                self.issue_date
            )
        )

        self.due_date_label.config(
            text=str(
                self.due_date
            )
        )

    # ==================================================
    # CHECK FORM FEE
    # ==================================================

    def check_form_fee(
        self,
        event=None
    ):

        selected = (
            self.borrower_combo.current()
        )

        if selected < 0:
            return

        borrower = (
            self.borrowers[selected]
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                fee_amount,
                payment_status

            FROM form_fees

            WHERE borrower_id = ?

            ORDER BY id DESC

            LIMIT 1
            """,
            (borrower["id"],)
        )

        fee = cursor.fetchone()

        connection.close()

        if fee is None:

            self.form_fee_label.config(
                text="❌ FORM FEE RECORD NOT FOUND"
            )

        elif fee["payment_status"] == "PAID":

            self.form_fee_label.config(
                text=(
                    f"✅ FORM FEE PAID "
                    f"(KSh "
                    f"{fee['fee_amount']:,.2f})"
                )
            )

        else:

            self.form_fee_label.config(
                text=(
                    f"❌ FORM FEE UNPAID "
                    f"(KSh "
                    f"{fee['fee_amount']:,.2f})"
                )
            )

    # ==================================================
    # CREATE LOAN
    # ==================================================

    def create_loan(self):

        selected = (
            self.borrower_combo.current()
        )

        if selected < 0:

            messagebox.showerror(
                "Error",
                "Please select a borrower."
            )

            return

        borrower = (
            self.borrowers[selected]
        )

        # ----------------------------------------------
        # PRINCIPAL
        # ----------------------------------------------

        try:

            principal = float(
                self.principal_entry.get()
            )

            if principal <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid loan amount."
            )

            return

        # ----------------------------------------------
        # FORM FEE
        # ----------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                fee_amount,
                payment_status

            FROM form_fees

            WHERE borrower_id = ?

            ORDER BY id DESC

            LIMIT 1
            """,
            (borrower["id"],)
        )

        fee = cursor.fetchone()

        connection.close()

        if fee is None:

            messagebox.showerror(
                "Form Fee Missing",
                "This borrower has no form fee record."
            )

            return

        if fee["payment_status"] != "PAID":

            messagebox.showerror(
                "Form Fee Not Paid",
                "The borrower must pay the form fee "
                "before a loan can be created."
            )

            return

        # ----------------------------------------------
        # COLLATERAL
        # ----------------------------------------------

        security_type = (
            self.security_type_entry
            .get()
            .strip()
        )

        description = (
            self.description_entry
            .get()
            .strip()
        )

        serial_number = (
            self.serial_entry
            .get()
            .strip()
        )

        if not security_type:

            messagebox.showerror(
                "Collateral Required",
                "Please enter the security type."
            )

            return

        if not description:

            messagebox.showerror(
                "Collateral Required",
                "Please describe the collateral."
            )

            return

        value_text = (
            self.collateral_value_entry
            .get()
            .strip()
        )

        try:

            collateral_value = float(
                value_text
            )

            if collateral_value < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid collateral value."
            )

            return

        # ----------------------------------------------
        # DATES
        # ----------------------------------------------

        issue = date.today()

        due = add_one_month(
            issue
        )

        issue_text = str(
            issue
        )

        due_text = str(
            due
        )

        monthly_interest = (
            principal
            * INTEREST_RATE
            / 100
        )

        # ----------------------------------------------
        # CONFIRMATION
        # ----------------------------------------------

        confirmed = messagebox.askyesno(
            "Confirm Loan",
            f"Borrower:\n"
            f"{borrower['full_name']}\n\n"

            f"Principal:\n"
            f"KSh {principal:,.2f}\n\n"

            f"Interest Rate:\n"
            f"{INTEREST_RATE:.0f}% per month\n\n"

            f"Monthly Interest:\n"
            f"KSh {monthly_interest:,.2f}\n\n"

            f"Date Borrowed:\n"
            f"{issue_text}\n\n"

            f"First Due Date:\n"
            f"{due_text}\n\n"

            f"Collateral:\n"
            f"{description}\n\n"

            "Create this loan?"
        )

        if not confirmed:
            return

        # ----------------------------------------------
        # SAVE
        # ----------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # ------------------------------------------
            # GENERATE LOAN NUMBER
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    COALESCE(
                        MAX(id),
                        0
                    ) + 1 AS next_number

                FROM loans
                """
            )

            next_number = (
                cursor.fetchone()
                ["next_number"]
            )

            loan_number = (
                f"LN-{next_number:04d}"
            )

            # ------------------------------------------
            # INSERT LOAN
            # ------------------------------------------

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
                    borrower["id"],
                    principal,
                    INTEREST_RATE,
                    issue_text,
                    due_text,
                    "ACTIVE"
                )
            )

            loan_id = (
                cursor.lastrowid
            )

            # ------------------------------------------
            # FIRST MONTHLY PERIOD
            # ------------------------------------------

            cursor.execute(
                """
                INSERT INTO monthly_periods (
                    loan_id,
                    month_start,
                    month_end,
                    opening_principal,
                    interest_due,
                    interest_paid,
                    principal_paid,
                    status
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    loan_id,
                    issue_text,
                    due_text,
                    principal,
                    monthly_interest,
                    0,
                    0,
                    "ACTIVE"
                )
            )

            # ------------------------------------------
            # COLLATERAL NUMBER
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    COALESCE(
                        MAX(id),
                        0
                    ) + 1 AS next_number

                FROM collateral
                """
            )

            collateral_number_value = (
                cursor.fetchone()
                ["next_number"]
            )

            collateral_number = (
                f"COL-{collateral_number_value:04d}"
            )

            # ------------------------------------------
            # SAVE COLLATERAL
            # ------------------------------------------

            cursor.execute(
                """
                INSERT INTO collateral (
                    collateral_number,
                    loan_id,
                    security_type,
                    description,
                    estimated_value,
                    serial_number,
                    condition,
                    date_received,
                    status,
                    notes
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    collateral_number,
                    loan_id,
                    security_type,
                    description,
                    collateral_value,
                    serial_number,
                    "",
                    issue_text,
                    "HELD",
                    ""
                )
            )

            connection.commit()

        except Exception as error:

            connection.rollback()

            connection.close()

            messagebox.showerror(
                "Database Error",
                "The loan could not be created.\n\n"
                f"{error}"
            )

            return

        connection.close()

        messagebox.showinfo(
            "Loan Created",
            f"Loan created successfully!\n\n"
            f"Loan Number: {loan_number}\n"
            f"Principal: "
            f"KSh {principal:,.2f}\n"
            f"Monthly Interest: "
            f"KSh {monthly_interest:,.2f}\n\n"
            f"Date Borrowed: "
            f"{issue_text}\n"
            f"Due Date: "
            f"{due_text}"
        )

        self.refresh_callback()

        self.window.destroy()


# ======================================================
# EDIT LOAN WINDOW
# ======================================================

class EditLoanWindow:

    def __init__(
        self,
        parent,
        loan,
        refresh_callback
    ):

        self.loan = loan

        self.refresh_callback = (
            refresh_callback
        )

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "MikopoHub - Edit Loan"
        )

        self.window.geometry(
            "500x560"
        )

        self.window.resizable(
            False,
            False
        )

        self.build_form()

    # ==================================================
    # EDIT FORM
    # ==================================================

    def build_form(self):

        container = tk.Frame(
            self.window,
            padx=30,
            pady=25
        )

        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="Edit Loan",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 20)
        )

        tk.Label(
            container,
            text=(
                f"Loan Number: "
                f"{self.loan['loan_number']}"
            )
        ).pack(
            pady=5
        )

        # ----------------------------------------------
        # CURRENT DATES
        # ----------------------------------------------

        tk.Label(
            container,
            text=(
                f"Date Borrowed: "
                f"{self.loan['issue_date']}"
            ),
            font=("Arial", 10)
        ).pack(
            pady=3
        )

        tk.Label(
            container,
            text=(
                f"Current Due Date: "
                f"{self.loan['due_date']}"
            ),
            font=("Arial", 10)
        ).pack(
            pady=3
        )

        # ----------------------------------------------
        # PRINCIPAL
        # ----------------------------------------------

        tk.Label(
            container,
            text="Principal (KSh)"
        ).pack(
            anchor="w",
            pady=(20, 0)
        )

        self.principal_entry = tk.Entry(
            container
        )

        self.principal_entry.insert(
            0,
            str(
                self.loan["principal"]
            )
        )

        self.principal_entry.pack(
            fill="x",
            pady=5
        )

        # ----------------------------------------------
        # STATUS
        # ----------------------------------------------

        tk.Label(
            container,
            text="Status"
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        self.status_var = tk.StringVar(
            value=self.loan["status"]
        )

        ttk.Combobox(
            container,
            textvariable=self.status_var,
            state="readonly",
            values=[
                "ACTIVE",
                "PAID",
                "PUSHED FORWARD",
                "DEFAULTED",
                "VOID"
            ]
        ).pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text=(
                "⚠️ Once payments exist, the "
                "principal cannot be changed."
            )
        ).pack(
            anchor="w",
            pady=10
        )

        tk.Button(
            container,
            text="SAVE CHANGES",
            font=("Arial", 11, "bold"),
            command=self.save_changes
        ).pack(
            fill="x",
            pady=20
        )

    # ==================================================
    # SAVE CHANGES
    # ==================================================

    def save_changes(self):

        try:

            principal = float(
                self.principal_entry.get()
            )

            if principal <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid principal amount."
            )

            return

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM payments
            WHERE loan_id = ?
            """,
            (self.loan["id"],)
        )

        payment_count = (
            cursor.fetchone()
            ["total"]
        )

        # ----------------------------------------------
        # PAYMENTS EXIST
        # ----------------------------------------------

        if payment_count > 0:

            cursor.execute(
                """
                UPDATE loans

                SET status = ?

                WHERE id = ?
                """,
                (
                    self.status_var.get(),
                    self.loan["id"]
                )
            )

            connection.commit()

            connection.close()

            messagebox.showinfo(
                "Updated",
                "Loan status updated.\n\n"
                "Principal and original loan dates "
                "were protected because payment "
                "history exists."
            )

            self.refresh_callback()

            self.window.destroy()

            return

        # ----------------------------------------------
        # NO PAYMENTS
        # ----------------------------------------------

        monthly_interest = (
            principal
            * INTEREST_RATE
            / 100
        )

        try:

            issue = date.fromisoformat(
                self.loan["issue_date"]
            )

        except (
            ValueError,
            TypeError
        ):

            issue = date.today()

        due = add_one_month(
            issue
        )

        cursor.execute(
            """
            UPDATE loans

            SET
                principal = ?,
                interest_rate = ?,
                issue_date = ?,
                due_date = ?,
                status = ?

            WHERE id = ?
            """,
            (
                principal,
                INTEREST_RATE,
                str(issue),
                str(due),
                self.status_var.get(),
                self.loan["id"]
            )
        )

        # ----------------------------------------------
        # UPDATE FIRST MONTHLY PERIOD
        # ----------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM monthly_periods

            WHERE loan_id = ?

            ORDER BY id

            LIMIT 1
            """,
            (self.loan["id"],)
        )

        period = cursor.fetchone()

        if period:

            cursor.execute(
                """
                UPDATE monthly_periods

                SET
                    month_start = ?,
                    month_end = ?,
                    opening_principal = ?,
                    interest_due = ?

                WHERE id = ?
                """,
                (
                    str(issue),
                    str(due),
                    principal,
                    monthly_interest,
                    period["id"]
                )
            )

        connection.commit()

        connection.close()

        messagebox.showinfo(
            "Updated",
            "Loan updated successfully.\n\n"
            f"Date Borrowed: {issue}\n"
            f"New Due Date: {due}"
        )

        self.refresh_callback()

        self.window.destroy()