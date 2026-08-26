
import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class BorrowerView:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("MikopoHub - Borrowers")
        self.window.geometry("1250x750")
        self.window.minsize(1050, 650)

        self.build_interface()

    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def build_interface(self):

        # ----------------------------------------------
        # HEADER
        # ----------------------------------------------

        header = tk.Frame(self.window)

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
            text="Borrowers",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Button(
            header,
            text="+ Add New Borrower",
            font=("Arial", 11, "bold"),
            command=self.open_add_borrower
        ).pack(
            side="right"
        )

        # ----------------------------------------------
        # SEARCH
        # ----------------------------------------------

        search_frame = tk.LabelFrame(
            self.window,
            text="Search Borrowers",
            padx=15,
            pady=12
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=55
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_borrowers
        )

        tk.Button(
            search_frame,
            text="🔍 Search",
            command=self.search_borrowers
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="✖ Clear",
            command=self.clear_search
        ).pack(
            side="left",
            padx=5
        )

        tk.Label(
            search_frame,
            text="Name • Phone • ID • Borrower No. • Location",
            font=("Arial", 9)
        ).pack(
            side="right"
        )

        # ----------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------

        actions = tk.Frame(self.window)

        actions.pack(
            fill="x",
            padx=25,
            pady=8
        )

        tk.Button(
            actions,
            text="👁 View Loan History",
            font=("Arial", 10, "bold"),
            command=self.view_loan_history
        ).pack(
            side="left",
            padx=5
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
            text="🗑️ Delete Selected",
            command=self.delete_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            actions,
            text="🔄 Refresh",
            command=self.load_borrowers
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------
        # BORROWER TABLE
        # ----------------------------------------------

        table_frame = tk.Frame(self.window)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = (
            "borrower_number",
            "full_name",
            "phone",
            "national_id",
            "location",
            "created_at"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "borrower_number": "Borrower No.",
            "full_name": "Full Name",
            "phone": "Phone",
            "national_id": "National ID",
            "location": "Location",
            "created_at": "Registered"
        }

        for column, heading in headings.items():

            self.table.heading(
                column,
                text=heading
            )

        widths = {
            "borrower_number": 110,
            "full_name": 220,
            "phone": 140,
            "national_id": 140,
            "location": 180,
            "created_at": 160
        }

        for column, width in widths.items():

            self.table.column(
                column,
                width=width
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

        self.table.bind(
            "<Double-1>",
            lambda event: self.view_loan_history()
        )

        self.table.bind(
            "<Return>",
            lambda event: self.view_loan_history()
        )

        self.load_borrowers()

    # ==================================================
    # BACK
    # ==================================================

    def go_back(self):

        self.window.destroy()

    # ==================================================
    # LOAD BORROWERS
    # ==================================================

    def load_borrowers(self):

        self.search_var.set("")

        self.fetch_borrowers("")

    # ==================================================
    # SEARCH BORROWERS
    # ==================================================

    def search_borrowers(self, event=None):

        search_text = (
            self.search_var
            .get()
            .strip()
        )

        self.fetch_borrowers(
            search_text
        )

    # ==================================================
    # FETCH BORROWERS
    # ==================================================

    def fetch_borrowers(self, search_text):

        connection = get_connection()
        cursor = connection.cursor()

        if search_text:

            pattern = f"%{search_text}%"

            cursor.execute(
                """
                SELECT
                    id,
                    borrower_number,
                    full_name,
                    phone,
                    national_id,
                    location,
                    created_at

                FROM borrowers

                WHERE
                    borrower_number LIKE ?
                    OR full_name LIKE ?
                    OR phone LIKE ?
                    OR national_id LIKE ?
                    OR location LIKE ?

                ORDER BY id DESC
                """,
                (
                    pattern,
                    pattern,
                    pattern,
                    pattern,
                    pattern
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    borrower_number,
                    full_name,
                    phone,
                    national_id,
                    location,
                    created_at

                FROM borrowers

                ORDER BY id DESC
                """
            )

        borrowers = cursor.fetchall()

        connection.close()

        # Clear table

        for row in self.table.get_children():

            self.table.delete(row)

        # Insert results

        for borrower in borrowers:

            self.table.insert(
                "",
                "end",
                iid=str(borrower["id"]),
                values=(
                    borrower["borrower_number"],
                    borrower["full_name"],
                    borrower["phone"],
                    borrower["national_id"] or "",
                    borrower["location"] or "",
                    borrower["created_at"]
                )
            )

    # ==================================================
    # CLEAR SEARCH
    # ==================================================

    def clear_search(self):

        self.search_var.set("")

        self.fetch_borrowers("")

        self.search_entry.focus_set()

    # ==================================================
    # GET SELECTED BORROWER
    # ==================================================

    def get_selected_id(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a borrower first."
            )

            return None

        return int(
            selected[0]
        )

    # ==================================================
    # GET BORROWER
    # ==================================================

    def get_borrower(self, borrower_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM borrowers
            WHERE id = ?
            """,
            (borrower_id,)
        )

        borrower = cursor.fetchone()

        connection.close()

        return borrower

    # ==================================================
    # VIEW LOAN HISTORY
    # ==================================================

    def view_loan_history(self):

        borrower_id = self.get_selected_id()

        if borrower_id is None:
            return

        borrower = self.get_borrower(
            borrower_id
        )

        if borrower is None:

            messagebox.showerror(
                "Error",
                "Borrower could not be found."
            )

            return

        BorrowerLoanHistoryWindow(
            self.window,
            borrower
        )

    # ==================================================
    # ADD BORROWER
    # ==================================================

    def open_add_borrower(self):

        AddBorrowerWindow(
            self.window,
            self.load_borrowers
        )

    # ==================================================
    # EDIT BORROWER
    # ==================================================

    def edit_selected(self):

        borrower_id = self.get_selected_id()

        if borrower_id is None:
            return

        borrower = self.get_borrower(
            borrower_id
        )

        if borrower is None:

            messagebox.showerror(
                "Error",
                "Borrower could not be found."
            )

            return

        EditBorrowerWindow(
            self.window,
            borrower,
            self.load_borrowers
        )

    # ==================================================
    # DELETE BORROWER
    # ==================================================

    def delete_selected(self):

        borrower_id = self.get_selected_id()

        if borrower_id is None:
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                borrower_number,
                full_name

            FROM borrowers

            WHERE id = ?
            """,
            (borrower_id,)
        )

        borrower = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS total

            FROM loans

            WHERE borrower_id = ?
            """,
            (borrower_id,)
        )

        loan_count = cursor.fetchone()["total"]

        connection.close()

        if borrower is None:
            return

        if loan_count > 0:

            messagebox.showwarning(
                "Borrower Protected",
                f"{borrower['full_name']} already has "
                "loan records.\n\n"
                "This borrower cannot be deleted."
            )

            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete this borrower?\n\n"
            f"Borrower No: "
            f"{borrower['borrower_number']}\n"
            f"Name: {borrower['full_name']}\n\n"
            "This action cannot be undone."
        )

        if not confirmed:
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM borrowers

            WHERE id = ?
            """,
            (borrower_id,)
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Borrower deleted successfully."
        )

        self.load_borrowers()


# ======================================================
# BORROWER LOAN HISTORY WINDOW
# ======================================================

class BorrowerLoanHistoryWindow:

    def __init__(self, parent, borrower):

        self.borrower = borrower

        self.window = tk.Toplevel(parent)

        self.window.title(
            f"MikopoHub - {borrower['full_name']} Loan History"
        )

        self.window.geometry(
            "1200x650"
        )

        self.window.minsize(
            1000,
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

        tk.Label(
            header,
            text="Loan History",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        # ----------------------------------------------
        # BORROWER INFORMATION
        # ----------------------------------------------

        info = tk.LabelFrame(
            self.window,
            text="Borrower",
            padx=15,
            pady=12
        )

        info.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            info,
            text=f"Name: {self.borrower['full_name']}",
            font=("Arial", 11, "bold")
        ).pack(
            side="left",
            padx=15
        )

        tk.Label(
            info,
            text=f"Borrower No: {self.borrower['borrower_number']}"
        ).pack(
            side="left",
            padx=15
        )

        tk.Label(
            info,
            text=f"Phone: {self.borrower['phone']}"
        ).pack(
            side="left",
            padx=15
        )

        # ----------------------------------------------
        # SUMMARY
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
            "Total Loans",
            "loan_count"
        )

        self.create_summary_card(
            summary,
            "Total Lent",
            "total_lent"
        )

        self.create_summary_card(
            summary,
            "Principal Returned",
            "principal_paid"
        )

        self.create_summary_card(
            summary,
            "Principal Remaining",
            "principal_remaining"
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
            pady=10
        )

        columns = (
            "loan_number",
            "issue_date",
            "principal",
            "principal_paid",
            "principal_remaining",
            "interest_rate",
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
            "issue_date": "Issue Date",
            "principal": "Original Principal",
            "principal_paid": "Principal Returned",
            "principal_remaining": "Principal Remaining",
            "interest_rate": "Interest Rate",
            "due_date": "Due Date",
            "status": "Status"
        }

        for column, heading in headings.items():

            self.table.heading(
                column,
                text=heading
            )

        widths = {
            "loan_number": 110,
            "issue_date": 110,
            "principal": 140,
            "principal_paid": 140,
            "principal_remaining": 150,
            "interest_rate": 100,
            "due_date": 110,
            "status": 100
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

    # ==================================================
    # SUMMARY CARD
    # ==================================================

    def create_summary_card(
        self,
        parent,
        title,
        key
    ):

        frame = tk.Frame(
            parent,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=10
        )

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
            font=("Arial", 13, "bold")
        )

        label.pack(
            pady=5
        )

        setattr(
            self,
            f"{key}_label",
            label
        )

    # ==================================================
    # LOAD LOANS
    # ==================================================

    def load_loans(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                loan_number,
                principal,
                interest_rate,
                issue_date,
                due_date,
                status

            FROM loans

            WHERE borrower_id = ?

            ORDER BY issue_date DESC, id DESC
            """,
            (
                self.borrower["id"],
            )
        )

        loans = cursor.fetchall()

        connection.close()

        for row in self.table.get_children():

            self.table.delete(row)

        total_lent = 0.0
        total_principal_paid = 0.0
        total_remaining = 0.0

        for loan in loans:

            loan_principal = float(
                loan["principal"] or 0
            )

            # ------------------------------------------
            # Calculate principal returned for this loan
            # ------------------------------------------

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COALESCE(
                    SUM(principal_portion),
                    0
                )

                FROM payments

                WHERE loan_id = ?
                """,
                (
                    loan["id"],
                )
            )

            principal_paid = (
                cursor.fetchone()[0] or 0
            )

            connection.close()

            principal_paid = float(
                principal_paid
            )

            principal_remaining = max(
                0,
                loan_principal - principal_paid
            )

            total_lent += loan_principal
            total_principal_paid += principal_paid
            total_remaining += principal_remaining

            self.table.insert(
                "",
                "end",
                iid=str(loan["id"]),
                values=(
                    loan["loan_number"],
                    loan["issue_date"],
                    self.money(loan_principal),
                    self.money(principal_paid),
                    self.money(principal_remaining),
                    f"{float(loan['interest_rate'] or 0):,.2f}%",
                    loan["due_date"] or "",
                    loan["status"]
                )
            )

        # ----------------------------------------------
        # UPDATE SUMMARY
        # ----------------------------------------------

        self.loan_count_label.config(
            text=str(len(loans))
        )

        self.total_lent_label.config(
            text=self.money(total_lent)
        )

        self.principal_paid_label.config(
            text=self.money(total_principal_paid)
        )

        self.principal_remaining_label.config(
            text=self.money(total_remaining)
        )

    # ==================================================
    # MONEY
    # ==================================================

    @staticmethod
    def money(amount):

        try:
            return f"KSh {float(amount):,.2f}"

        except Exception:
            return "KSh 0.00"


# ======================================================
# ADD BORROWER WINDOW
# ======================================================

class AddBorrowerWindow:

    def __init__(
        self,
        parent,
        refresh_callback
    ):

        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)

        self.window.title(
            "MikopoHub - Add Borrower"
        )

        self.window.geometry(
            "550x650"
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
            text="Add New Borrower",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 25)
        )

        tk.Label(
            container,
            text="Full Name"
        ).pack(
            anchor="w"
        )

        self.name_entry = tk.Entry(
            container
        )

        self.name_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Label(
            container,
            text="Phone Number"
        ).pack(
            anchor="w"
        )

        self.phone_entry = tk.Entry(
            container
        )

        self.phone_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Label(
            container,
            text="National ID"
        ).pack(
            anchor="w"
        )

        self.id_entry = tk.Entry(
            container
        )

        self.id_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Label(
            container,
            text="Location"
        ).pack(
            anchor="w"
        )

        self.location_entry = tk.Entry(
            container
        )

        self.location_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Label(
            container,
            text="Form Fee",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        self.loan_amount_entry = tk.Entry(
            container
        )

        self.loan_amount_entry.insert(
            0,
            "0"
        )

        self.loan_amount_entry.pack(
            fill="x",
            pady=5
        )

        self.loan_amount_entry.bind(
            "<KeyRelease>",
            self.calculate_form_fee
        )

        self.form_fee_label = tk.Label(
            container,
            text="Form Fee: KSh 0.00"
        )

        self.form_fee_label.pack(
            anchor="w",
            pady=5
        )

        self.form_fee_status = tk.StringVar(
            value="UNPAID"
        )

        ttk.Combobox(
            container,
            textvariable=self.form_fee_status,
            state="readonly",
            values=[
                "PAID",
                "UNPAID"
            ]
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="SAVE BORROWER",
            font=("Arial", 11, "bold"),
            command=self.save_borrower
        ).pack(
            fill="x",
            pady=25
        )

    # ==================================================
    # FORM FEE
    # ==================================================

    def calculate_form_fee(self, event=None):

        try:
            amount = float(
                self.loan_amount_entry.get()
            )

        except ValueError:
            amount = 0

        fee = self.get_form_fee(
            amount
        )

        self.form_fee_label.config(
            text=f"Form Fee: KSh {fee:,.2f}"
        )

    @staticmethod
    def get_form_fee(amount):

        if amount <= 1000:
            return 200

        elif amount <= 5000:
            return 500

        else:
            return 1000

    # ==================================================
    # SAVE BORROWER
    # ==================================================

    def save_borrower(self):

        full_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        national_id = self.id_entry.get().strip()
        location = self.location_entry.get().strip()

        if not full_name:

            messagebox.showerror(
                "Error",
                "Please enter the borrower's full name."
            )

            return

        if not phone:

            messagebox.showerror(
                "Error",
                "Please enter the phone number."
            )

            return

        try:

            requested_amount = float(
                self.loan_amount_entry.get()
            )

            if requested_amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid intended loan amount."
            )

            return

        fee_amount = self.get_form_fee(
            requested_amount
        )

        confirmed = messagebox.askyesno(
            "Confirm Borrower",
            f"Name:\n{full_name}\n\n"
            f"Phone:\n{phone}\n\n"
            f"National ID:\n"
            f"{national_id or 'Not provided'}\n\n"
            f"Location:\n"
            f"{location or 'Not provided'}\n\n"
            f"Requested Loan:\n"
            f"KSh {requested_amount:,.2f}\n\n"
            f"Form Fee:\n"
            f"KSh {fee_amount:,.2f}\n\n"
            f"Form Fee Status:\n"
            f"{self.form_fee_status.get()}\n\n"
            "Save this borrower?"
        )

        if not confirmed:
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    COALESCE(
                        MAX(id),
                        0
                    ) + 1 AS next_number

                FROM borrowers
                """
            )

            next_number = (
                cursor.fetchone()["next_number"]
            )

            borrower_number = (
                f"BRW-{next_number:04d}"
            )

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

            cursor.execute(
                """
                INSERT INTO form_fees (
                    borrower_id,
                    requested_amount,
                    fee_amount,
                    payment_status,
                    payment_method,
                    reference_number,
                    payment_date
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    borrower_id,
                    requested_amount,
                    fee_amount,
                    self.form_fee_status.get(),
                    None,
                    None,
                    None
                )
            )

            connection.commit()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not create borrower.\n\n{error}"
            )

            return

        finally:

            connection.close()

        messagebox.showinfo(
            "Borrower Created",
            f"Borrower created successfully!\n\n"
            f"Borrower Number:\n"
            f"{borrower_number}\n\n"
            f"Form Fee:\n"
            f"KSh {fee_amount:,.2f}\n\n"
            f"Status:\n"
            f"{self.form_fee_status.get()}"
        )

        self.refresh_callback()

        self.window.destroy()


# ======================================================
# EDIT BORROWER WINDOW
# ======================================================

class EditBorrowerWindow:

    def __init__(
        self,
        parent,
        borrower,
        refresh_callback
    ):

        self.borrower = borrower
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)

        self.window.title(
            "MikopoHub - Edit Borrower"
        )

        self.window.geometry(
            "550x550"
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
            text="Edit Borrower",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 20)
        )

        tk.Label(
            container,
            text=(
                f"Borrower Number: "
                f"{self.borrower['borrower_number']}"
            )
        ).pack(
            pady=5
        )

        tk.Label(
            container,
            text="Full Name"
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        self.name_entry = tk.Entry(
            container
        )

        self.name_entry.insert(
            0,
            self.borrower["full_name"]
        )

        self.name_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="Phone Number"
        ).pack(
            anchor="w",
            pady=(10, 0)
        )

        self.phone_entry = tk.Entry(
            container
        )

        self.phone_entry.insert(
            0,
            self.borrower["phone"]
        )

        self.phone_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="National ID"
        ).pack(
            anchor="w",
            pady=(10, 0)
        )

        self.id_entry = tk.Entry(
            container
        )

        self.id_entry.insert(
            0,
            self.borrower["national_id"] or ""
        )

        self.id_entry.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            container,
            text="Location"
        ).pack(
            anchor="w",
            pady=(10, 0)
        )

        self.location_entry = tk.Entry(
            container
        )

        self.location_entry.insert(
            0,
            self.borrower["location"] or ""
        )

        self.location_entry.pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="SAVE CHANGES",
            font=("Arial", 11, "bold"),
            command=self.save_changes
        ).pack(
            fill="x",
            pady=25
        )

    # ==================================================
    # SAVE CHANGES
    # ==================================================

    def save_changes(self):

        full_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        national_id = self.id_entry.get().strip()
        location = self.location_entry.get().strip()

        if not full_name:

            messagebox.showerror(
                "Error",
                "Full name cannot be empty."
            )

            return

        if not phone:

            messagebox.showerror(
                "Error",
                "Phone number cannot be empty."
            )

            return

        confirmed = messagebox.askyesno(
            "Confirm Changes",
            "Save these changes to the borrower?"
        )

        if not confirmed:
            return

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE borrowers

                SET
                    full_name = ?,
                    phone = ?,
                    national_id = ?,
                    location = ?

                WHERE id = ?
                """,
                (
                    full_name,
                    phone,
                    national_id,
                    location,
                    self.borrower["id"]
                )
            )

            connection.commit()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Update Error",
                f"Could not update borrower.\n\n{error}"
            )

            return

        finally:

            connection.close()

        messagebox.showinfo(
            "Updated",
            "Borrower information updated successfully."
        )

        self.refresh_callback()

        self.window.destroy()
