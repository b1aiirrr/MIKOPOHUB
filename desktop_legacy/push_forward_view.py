import tkinter as tk
from tkinter import messagebox
from datetime import date
import calendar

from database import get_connection


INTEREST_RATE = 20.0


def add_one_month(original_date):
    """
    Add one calendar month while correctly handling
    dates such as 31 January.
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


class PushForwardView:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)

        self.window.title(
            "MikopoHub - Push Forward"
        )

        self.window.geometry(
            "1050x650"
        )

        self.window.minsize(
            900,
            550
        )

        self.build_interface()

        self.load_loans()

    # ==================================================
    # INTERFACE
    # ==================================================

    def build_interface(self):

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
            text="← Back to Dashboard",
            font=("Arial", 10, "bold"),
            command=self.go_back
        ).pack(
            side="left",
            padx=(0, 20)
        )

        tk.Label(
            header,
            text="Push Forward",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        # ----------------------------------------------
        # INFORMATION
        # ----------------------------------------------

        info = tk.Frame(
            self.window,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=12
        )

        info.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        tk.Label(
            info,
            text=(
                "Push Forward allows the remaining principal "
                "to continue into the next calendar month. "
                "The current month's interest must be fully paid "
                "before the principal can be pushed forward."
            ),
            font=("Arial", 10),
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------
        # LOAN SELECTION
        # ----------------------------------------------

        selection = tk.Frame(
            self.window
        )

        selection.pack(
            fill="x",
            padx=25,
            pady=10
        )

        tk.Label(
            selection,
            text="Select Loan:",
            font=("Arial", 11, "bold")
        ).pack(
            side="left"
        )

        self.loan_var = tk.StringVar()

        self.loan_menu = tk.OptionMenu(
            selection,
            self.loan_var,
            ""
        )

        self.loan_menu.config(
            width=50
        )

        self.loan_menu.pack(
            side="left",
            padx=15
        )

        tk.Button(
            selection,
            text="🔄 Refresh",
            command=self.load_loans
        ).pack(
            side="left"
        )

        # ----------------------------------------------
        # DETAILS
        # ----------------------------------------------

        details_frame = tk.LabelFrame(
            self.window,
            text="Current Loan Period",
            padx=20,
            pady=15
        )

        details_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.details_label = tk.Label(
            details_frame,
            text="Select a loan to view details.",
            font=("Arial", 11),
            justify="left"
        )

        self.details_label.pack(
            anchor="w"
        )

        # ----------------------------------------------
        # PUSH BUTTON
        # ----------------------------------------------

        self.push_button = tk.Button(
            self.window,
            text="🔄 PUSH FORWARD",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=12,
            command=self.push_forward
        )

        self.push_button.pack(
            pady=15
        )

        # ----------------------------------------------
        # HISTORY
        # ----------------------------------------------

        tk.Label(
            self.window,
            text="Push Forward History",
            font=("Arial", 15, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(10, 5)
        )

        history_frame = tk.Frame(
            self.window
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        self.history = tk.Text(
            history_frame,
            height=10,
            state="disabled",
            wrap="word"
        )

        scrollbar = tk.Scrollbar(
            history_frame,
            command=self.history.yview
        )

        self.history.configure(
            yscrollcommand=scrollbar.set
        )

        self.history.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.loan_var.trace_add(
            "write",
            self.loan_selected
        )

    # ==================================================
    # LOAD ACTIVE LOANS
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
                loans.interest_rate,
                loans.status,
                borrowers.full_name

            FROM loans

            JOIN borrowers
                ON borrowers.id = loans.borrower_id

            WHERE loans.status = 'ACTIVE'

            ORDER BY loans.id DESC
            """
        )

        loans = cursor.fetchall()

        connection.close()

        menu = self.loan_menu["menu"]

        menu.delete(
            0,
            "end"
        )

        self.loan_data = {}

        for loan in loans:

            display = (
                f"{loan['loan_number']} - "
                f"{loan['full_name']} - "
                f"KSh {loan['principal']:,.2f}"
            )

            self.loan_data[display] = loan

            menu.add_command(
                label=display,
                command=lambda value=display:
                self.loan_var.set(value)
            )

        if loans:

            first = (
                f"{loans[0]['loan_number']} - "
                f"{loans[0]['full_name']} - "
                f"KSh {loans[0]['principal']:,.2f}"
            )

            self.loan_var.set(
                first
            )

        else:

            self.loan_var.set("")

            self.details_label.config(
                text="No active loans found."
            )

            self.clear_history()

    # ==================================================
    # LOAN SELECTED
    # ==================================================

    def loan_selected(
        self,
        *args
    ):

        selected = self.loan_var.get()

        if not selected:
            return

        if selected not in self.loan_data:
            return

        loan = self.loan_data[selected]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                month_start,
                month_end,
                opening_principal,
                interest_due,
                interest_paid,
                principal_paid,
                status

            FROM monthly_periods

            WHERE loan_id = ?

            ORDER BY id DESC

            LIMIT 1
            """,
            (loan["id"],)
        )

        period = cursor.fetchone()

        connection.close()

        if period is None:

            self.details_label.config(
                text=(
                    f"Loan: {loan['loan_number']}\n"
                    f"Borrower: {loan['full_name']}\n\n"
                    "No monthly period found."
                )
            )

            self.clear_history()

            return

        remaining_interest = max(
            0,
            period["interest_due"]
            - period["interest_paid"]
        )

        remaining_principal = max(
            0,
            period["opening_principal"]
            - period["principal_paid"]
        )

        new_interest = (
            remaining_principal
            * loan["interest_rate"]
            / 100
        )

        if remaining_interest <= 0.01:

            eligibility = (
                "✅ READY TO PUSH FORWARD"
            )

        else:

            eligibility = (
                "❌ INTEREST MUST BE PAID FIRST"
            )

        text = (
            f"Loan: {loan['loan_number']}\n"
            f"Borrower: {loan['full_name']}\n\n"

            f"Current Period: "
            f"{period['month_start']} → "
            f"{period['month_end']}\n\n"

            f"Opening Principal: "
            f"KSh {period['opening_principal']:,.2f}\n"

            f"Principal Paid: "
            f"KSh {period['principal_paid']:,.2f}\n"

            f"Remaining Principal: "
            f"KSh {remaining_principal:,.2f}\n\n"

            f"Interest Due: "
            f"KSh {period['interest_due']:,.2f}\n"

            f"Interest Paid: "
            f"KSh {period['interest_paid']:,.2f}\n"

            f"Remaining Interest: "
            f"KSh {remaining_interest:,.2f}\n\n"

            f"Next Monthly Interest: "
            f"KSh {new_interest:,.2f}\n\n"

            f"Status: {eligibility}"
        )

        self.details_label.config(
            text=text
        )

        self.load_history(
            loan["id"]
        )

    # ==================================================
    # LOAD HISTORY
    # ==================================================

    def load_history(
        self,
        loan_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                push_date,
                principal_carried

            FROM push_forward_history

            WHERE loan_id = ?

            ORDER BY id DESC
            """,
            (loan_id,)
        )

        rows = cursor.fetchall()

        connection.close()

        self.history.config(
            state="normal"
        )

        self.history.delete(
            "1.0",
            "end"
        )

        if not rows:

            self.history.insert(
                "end",
                "No push forward history found."
            )

        else:

            for row in rows:

                self.history.insert(
                    "end",
                    (
                        f"{row['push_date']}   |   "
                        f"Principal carried: "
                        f"KSh "
                        f"{row['principal_carried']:,.2f}\n"
                    )
                )

        self.history.config(
            state="disabled"
        )

    # ==================================================
    # CLEAR HISTORY
    # ==================================================

    def clear_history(self):

        self.history.config(
            state="normal"
        )

        self.history.delete(
            "1.0",
            "end"
        )

        self.history.insert(
            "end",
            "No push forward history found."
        )

        self.history.config(
            state="disabled"
        )

    # ==================================================
    # PUSH FORWARD
    # ==================================================

    def push_forward(self):

        selected = self.loan_var.get()

        if not selected:

            messagebox.showwarning(
                "No Loan Selected",
                "Please select a loan first."
            )

            return

        if selected not in self.loan_data:

            messagebox.showwarning(
                "Invalid Loan",
                "Please select a valid loan."
            )

            return

        loan = self.loan_data[selected]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # ------------------------------------------
            # GET CURRENT PERIOD
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    id,
                    month_start,
                    month_end,
                    opening_principal,
                    interest_due,
                    interest_paid,
                    principal_paid,
                    status

                FROM monthly_periods

                WHERE loan_id = ?

                ORDER BY id DESC

                LIMIT 1
                """,
                (loan["id"],)
            )

            period = cursor.fetchone()

            if period is None:

                messagebox.showerror(
                    "Error",
                    "No monthly period exists for this loan."
                )

                connection.close()

                return

            # ------------------------------------------
            # MAKE SURE PERIOD IS ACTIVE
            # ------------------------------------------

            if period["status"] != "ACTIVE":

                messagebox.showerror(
                    "Invalid Period",
                    (
                        "The latest monthly period is not active.\n\n"
                        f"Current status: {period['status']}"
                    )
                )

                connection.close()

                return

            # ------------------------------------------
            # CALCULATE REMAINING BALANCES
            # ------------------------------------------

            remaining_interest = max(
                0,
                period["interest_due"]
                - period["interest_paid"]
            )

            remaining_principal = max(
                0,
                period["opening_principal"]
                - period["principal_paid"]
            )

            # ------------------------------------------
            # INTEREST MUST BE PAID
            # ------------------------------------------

            if remaining_interest > 0.01:

                connection.close()

                messagebox.showwarning(
                    "Interest Not Fully Paid",
                    (
                        "Push Forward is not allowed yet.\n\n"
                        f"Remaining interest:\n"
                        f"KSh {remaining_interest:,.2f}\n\n"
                        "The borrower must fully pay the "
                        "current month's interest first."
                    )
                )

                return

            # ------------------------------------------
            # CHECK PRINCIPAL
            # ------------------------------------------

            if remaining_principal <= 0.01:

                connection.close()

                messagebox.showinfo(
                    "Loan Completed",
                    (
                        "There is no remaining principal "
                        "to push forward."
                    )
                )

                return

            # ------------------------------------------
            # NEW MONTHLY INTEREST
            # ------------------------------------------

            interest_rate = (
                loan["interest_rate"]
            )

            new_interest = (
                remaining_principal
                * interest_rate
                / 100
            )

            # ------------------------------------------
            # CALCULATE NEW CALENDAR DATES
            # ------------------------------------------

            try:

                old_end = date.fromisoformat(
                    period["month_end"]
                )

            except (
                ValueError,
                TypeError
            ):

                old_end = date.today()

            new_start = old_end

            new_end = add_one_month(
                new_start
            )

            # ------------------------------------------
            # CONFIRM
            # ------------------------------------------

            confirmed = messagebox.askyesno(
                "Confirm Push Forward",
                (
                    f"Borrower:\n"
                    f"{loan['full_name']}\n\n"

                    f"Loan:\n"
                    f"{loan['loan_number']}\n\n"

                    f"Principal carried forward:\n"
                    f"KSh {remaining_principal:,.2f}\n\n"

                    f"New monthly interest:\n"
                    f"KSh {new_interest:,.2f}\n\n"

                    f"New period:\n"
                    f"{new_start} → {new_end}\n\n"

                    "Push this principal forward?"
                )
            )

            if not confirmed:

                connection.close()

                return

            # ------------------------------------------
            # COMPLETE CURRENT PERIOD
            # ------------------------------------------

            cursor.execute(
                """
                UPDATE monthly_periods

                SET status = 'COMPLETED'

                WHERE id = ?
                """,
                (period["id"],)
            )

            # ------------------------------------------
            # CREATE NEW PERIOD
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

                VALUES (?, ?, ?, ?, ?, 0, 0, 'ACTIVE')
                """,
                (
                    loan["id"],
                    str(new_start),
                    str(new_end),
                    remaining_principal,
                    new_interest
                )
            )

            new_period_id = (
                cursor.lastrowid
            )

            # ------------------------------------------
            # UPDATE LOAN DUE DATE
            # ------------------------------------------

            cursor.execute(
                """
                UPDATE loans

                SET
                    due_date = ?,
                    status = 'ACTIVE'

                WHERE id = ?
                """,
                (
                    str(new_end),
                    loan["id"]
                )
            )

            # ------------------------------------------
            # SAVE HISTORY
            # ------------------------------------------

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
                    loan["id"],
                    period["id"],
                    new_period_id,
                    remaining_principal,
                    datetime_now()
                )
            )

            connection.commit()

            connection.close()

            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            messagebox.showinfo(
                "Push Forward Successful",
                (
                    "Push Forward completed successfully.\n\n"

                    f"Principal carried forward:\n"
                    f"KSh {remaining_principal:,.2f}\n\n"

                    f"New monthly interest:\n"
                    f"KSh {new_interest:,.2f}\n\n"

                    f"New period:\n"
                    f"{new_start} → {new_end}"
                )
            )

            self.load_loans()

        except Exception as error:

            connection.rollback()
            connection.close()

            messagebox.showerror(
                "Push Forward Error",
                (
                    "The Push Forward operation failed.\n\n"
                    f"{error}"
                )
            )

    # ==================================================
    # BACK
    # ==================================================

    def go_back(self):

        self.window.destroy()


def datetime_now():

    from datetime import datetime

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )