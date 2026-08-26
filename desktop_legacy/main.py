
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime

from database import (
    initialize_database,
    get_connection
)

from borrower_view import BorrowerView
from loan_view import LoanView
from payment_view import PaymentView
from push_forward_view import PushForwardView
from collateral_view import CollateralView

from admin_service import (
    ensure_admin_settings,
    verify_admin_password,
    change_admin_password
)

from reset_database import reset_database


# ======================================================
# MIKOPOHUB APPLICATION
# ======================================================

class MikopoHubApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "MikopoHub - Personal Lending System"
        )

        self.root.geometry(
            "1100x650"
        )

        self.root.minsize(
            900,
            550
        )

        self.build_interface()


    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def build_interface(self):

        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------

        header = tk.Frame(
            self.root,
            height=70
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="MIKOPOHUB",
            font=("Arial", 24, "bold")
        ).pack(
            side="left",
            padx=25,
            pady=15
        )

        tk.Label(
            header,
            text="Personal Lending Management System",
            font=("Arial", 11)
        ).pack(
            side="left",
            padx=10
        )

        # ------------------------------------------------
        # MAIN AREA
        # ------------------------------------------------

        main_frame = tk.Frame(
            self.root
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------
        # SIDEBAR
        # ------------------------------------------------

        sidebar = tk.Frame(
            main_frame,
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # ------------------------------------------------
        # DASHBOARD
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="🏠 Dashboard",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.show_dashboard
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # BORROWERS
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="👤 Borrowers",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_borrowers
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # LOANS
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="💰 Loans",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_loans
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # PAYMENTS
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="💳 Payments",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_payments
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # PUSH FORWARD
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="🔄 Push Forward",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_push_forward
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # COLLATERAL
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="🔐 Collateral",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_collateral
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # EXCEL / REPORTS
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="📗 Excel",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_excel
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # ADMIN
        # ------------------------------------------------

        tk.Button(
            sidebar,
            text="🔐 Admin",
            font=("Arial", 11),
            anchor="w",
            padx=20,
            pady=12,
            command=self.open_admin
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )

        # ------------------------------------------------
        # CONTENT AREA
        # ------------------------------------------------

        self.content = tk.Frame(
            main_frame
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_dashboard()


    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        for widget in self.content.winfo_children():

            widget.destroy()

        dashboard = tk.Frame(
            self.content
        )

        dashboard.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        # ------------------------------------------------
        # TITLE
        # ------------------------------------------------

        title_frame = tk.Frame(
            dashboard
        )

        title_frame.pack(
            fill="x"
        )

        tk.Label(
            title_frame,
            text="Dashboard",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        # ------------------------------------------------
        # DASHBOARD BUTTONS
        # ------------------------------------------------

        button_frame = tk.Frame(
            title_frame
        )

        button_frame.pack(
            side="right"
        )

        tk.Button(
            button_frame,
            text="📥 Download Report",
            command=self.open_download_window
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.show_dashboard
        ).pack(
            side="left",
            padx=5
        )

        tk.Label(
            dashboard,
            text="Welcome to MikopoHub",
            font=("Arial", 12)
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        # ------------------------------------------------
        # GET LIVE DATABASE INFORMATION
        # ------------------------------------------------

        stats = self.get_dashboard_statistics()

        # ------------------------------------------------
        # FIRST ROW
        # ------------------------------------------------

        row_one = tk.Frame(
            dashboard
        )

        row_one.pack(
            fill="x",
            pady=5
        )

        self.create_card(
            row_one,
            "👥 Borrowers",
            str(stats["borrowers"])
        )

        self.create_card(
            row_one,
            "💰 Active Loans",
            str(stats["active_loans"])
        )

        self.create_card(
            row_one,
            "💵 Total Lent",
            self.money(stats["total_lent"])
        )

        # ------------------------------------------------
        # SECOND ROW
        # ------------------------------------------------

        row_two = tk.Frame(
            dashboard
        )

        row_two.pack(
            fill="x",
            pady=5
        )

        self.create_card(
            row_two,
            "📌 Principal Outstanding",
            self.money(stats["outstanding"])
        )

        self.create_card(
            row_two,
            "📈 Interest Collected",
            self.money(stats["interest_collected"])
        )

        self.create_card(
            row_two,
            "🧾 Form Fees",
            self.money(stats["form_fees"])
        )

        # ------------------------------------------------
        # THIRD ROW
        # ------------------------------------------------

        row_three = tk.Frame(
            dashboard
        )

        row_three.pack(
            fill="x",
            pady=5
        )

        self.create_card(
            row_three,
            "📅 Due Today",
            str(stats["due_today"])
        )

        self.create_card(
            row_three,
            "⚠️ Overdue",
            str(stats["overdue"])
        )

        self.create_card(
            row_three,
            "🔐 Collateral Held",
            str(stats["collateral_held"])
        )

        # ------------------------------------------------
        # TODAY'S PAYMENTS
        # ------------------------------------------------

        payment_frame = tk.Frame(
            dashboard,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=12
        )

        payment_frame.pack(
            fill="x",
            pady=(15, 5)
        )

        tk.Label(
            payment_frame,
            text="Today's Payments",
            font=("Arial", 11, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            payment_frame,
            text=self.money(
                stats["today_payments"]
            ),
            font=("Arial", 16, "bold")
        ).pack(
            side="right"
        )


    # ==================================================
    # DOWNLOAD WINDOW
    # ==================================================

    def open_download_window(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Download MikopoHub Report"
        )

        window.geometry(
            "500x500"
        )

        window.resizable(
            False,
            False
        )

        window.transient(
            self.root
        )

        window.grab_set()

        container = tk.Frame(
            window,
            padx=30,
            pady=30
        )

        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="📥 Download Reports",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 10)
        )

        tk.Label(
            container,
            text=(
                "Select the information you want to "
                "download as a CSV file.\n\n"
                "CSV files can be opened and printed "
                "using Microsoft Excel."
            ),
            justify="center"
        ).pack(
            pady=(0, 20)
        )

        tk.Button(
            container,
            text="👥 Download Borrowers",
            font=("Arial", 11),
            command=lambda: self.download_report(
                "borrowers"
            )
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="💰 Download Loans",
            font=("Arial", 11),
            command=lambda: self.download_report(
                "loans"
            )
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="💳 Download Payments",
            font=("Arial", 11),
            command=lambda: self.download_report(
                "payments"
            )
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="🔐 Download Collateral",
            font=("Arial", 11),
            command=lambda: self.download_report(
                "collateral"
            )
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            container,
            text="📊 Download Complete Summary",
            font=("Arial", 11, "bold"),
            command=lambda: self.download_report(
                "summary"
            )
        ).pack(
            fill="x",
            pady=15
        )

        tk.Button(
            container,
            text="Close",
            command=window.destroy
        ).pack(
            fill="x",
            pady=5
        )


    # ==================================================
    # DOWNLOAD REPORT
    # ==================================================

    def download_report(self, report_type):

        file_path = filedialog.asksaveasfilename(
            title="Save MikopoHub Report",
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:

            return

        # =================================================
        # COMPLETE SUMMARY
        # =================================================
        #
        # IMPORTANT:
        # Summary uses get_dashboard_statistics(),
        # which opens and closes its own database connection.
        # Therefore, do not open another database connection
        # before creating the summary.
        #

        if report_type == "summary":

            try:

                stats = self.get_dashboard_statistics()

                rows = [

                    (
                        "Total Borrowers",
                        stats["borrowers"]
                    ),

                    (
                        "Active Loans",
                        stats["active_loans"]
                    ),

                    (
                        "Total Lent",
                        stats["total_lent"]
                    ),

                    (
                        "Principal Outstanding",
                        stats["outstanding"]
                    ),

                    (
                        "Interest Collected",
                        stats["interest_collected"]
                    ),

                    (
                        "Form Fees",
                        stats["form_fees"]
                    ),

                    (
                        "Due Today",
                        stats["due_today"]
                    ),

                    (
                        "Overdue Loans",
                        stats["overdue"]
                    ),

                    (
                        "Collateral Held",
                        stats["collateral_held"]
                    ),

                    (
                        "Today's Payments",
                        stats["today_payments"]
                    )
                ]

                headers = [
                    "Description",
                    "Value"
                ]

                report_title = "MikopoHub Complete Summary"

                self.write_csv_report(
                    file_path,
                    report_title,
                    headers,
                    rows
                )

            except Exception as error:

                messagebox.showerror(
                    "Download Error",
                    f"Unable to create the summary report.\n\n"
                    f"Error:\n{error}"
                )

            return

        # =================================================
        # DATABASE REPORTS
        # =================================================

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ------------------------------------------------
            # BORROWERS
            # ------------------------------------------------

            if report_type == "borrowers":

                cursor.execute("""
                    SELECT *
                    FROM borrowers
                """)

                rows = cursor.fetchall()

                headers = [
                    description[0]
                    for description in cursor.description
                ]

                report_title = "MikopoHub Borrowers Report"


            # ------------------------------------------------
            # LOANS
            # ------------------------------------------------

            elif report_type == "loans":

                cursor.execute("""
                    SELECT
                        l.*,
                        b.full_name
                    FROM loans l
                    LEFT JOIN borrowers b
                    ON l.borrower_id = b.id
                """)

                rows = cursor.fetchall()

                headers = [
                    description[0]
                    for description in cursor.description
                ]

                report_title = "MikopoHub Loans Report"


            # ------------------------------------------------
            # PAYMENTS
            # ------------------------------------------------

            elif report_type == "payments":

                cursor.execute("""
                    SELECT
                        p.*,
                        b.full_name
                    FROM payments p
                    LEFT JOIN loans l
                    ON p.loan_id = l.id
                    LEFT JOIN borrowers b
                    ON l.borrower_id = b.id
                """)

                rows = cursor.fetchall()

                headers = [
                    description[0]
                    for description in cursor.description
                ]

                report_title = "MikopoHub Payments Report"


            # ------------------------------------------------
            # COLLATERAL
            # ------------------------------------------------

            elif report_type == "collateral":

                cursor.execute("""
                    SELECT
                        c.*,
                        b.full_name
                    FROM collateral c
                    LEFT JOIN loans l
                    ON c.loan_id = l.id
                    LEFT JOIN borrowers b
                    ON l.borrower_id = b.id
                """)

                rows = cursor.fetchall()

                headers = [
                    description[0]
                    for description in cursor.description
                ]

                report_title = "MikopoHub Collateral Report"


            else:

                messagebox.showerror(
                    "Report Error",
                    "Unknown report type."
                )

                return

            # ------------------------------------------------
            # WRITE CSV REPORT
            # ------------------------------------------------

            self.write_csv_report(
                file_path,
                report_title,
                headers,
                rows
            )

        except Exception as error:

            messagebox.showerror(
                "Download Error",
                f"Unable to create the report.\n\n"
                f"Error:\n{error}"
            )

        finally:

            if connection:

                connection.close()


    # ==================================================
    # WRITE CSV REPORT
    # ==================================================

    def write_csv_report(
        self,
        file_path,
        report_title,
        headers,
        rows
    ):

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(
                [report_title]
            )

            writer.writerow(
                [
                    "Generated:",
                    datetime.now().strftime(
                        "%d %B %Y %H:%M:%S"
                    )
                ]
            )

            writer.writerow(
                []
            )

            writer.writerow(
                headers
            )

            for row in rows:

                writer.writerow(
                    row
                )

        messagebox.showinfo(
            "Download Complete",
            f"{report_title} has been saved successfully.\n\n"
            f"Location:\n{file_path}\n\n"
            "You can now open the file using "
            "Microsoft Excel and print it."
        )


    # ==================================================
    # DASHBOARD CARD
    # ==================================================

    def create_card(
        self,
        parent,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=12
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
            font=("Arial", 10)
        ).pack()

        tk.Label(
            card,
            text=value,
            font=("Arial", 17, "bold")
        ).pack(
            pady=5
        )


    # ==================================================
    # MONEY FORMAT
    # ==================================================

    def money(self, amount):

        try:

            return f"KSh {float(amount):,.2f}"

        except Exception:

            return "KSh 0.00"


    # ==================================================
    # GET DASHBOARD STATISTICS
    # ==================================================

    def get_dashboard_statistics(self):

        stats = {
            "borrowers": 0,
            "active_loans": 0,
            "total_lent": 0,
            "outstanding": 0,
            "interest_collected": 0,
            "form_fees": 0,
            "due_today": 0,
            "overdue": 0,
            "collateral_held": 0,
            "today_payments": 0
        }

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM borrowers
            """)

            stats["borrowers"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM loans
                WHERE status = 'ACTIVE'
            """)

            stats["active_loans"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(principal),
                    0
                )
                FROM loans
                WHERE status != 'VOID'
            """)

            stats["total_lent"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(principal),
                    0
                )
                FROM loans
                WHERE status = 'ACTIVE'
            """)

            active_principal = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(principal_portion),
                    0
                )
                FROM payments
            """)

            principal_paid = (
                cursor.fetchone()[0] or 0
            )

            stats["outstanding"] = max(
                0,
                active_principal - principal_paid
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(interest_portion),
                    0
                )
                FROM payments
            """)

            stats["interest_collected"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(fee_amount),
                    0
                )
                FROM form_fees
                WHERE payment_status = 'PAID'
            """)

            stats["form_fees"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM loans
                WHERE
                    status = 'ACTIVE'
                    AND due_date = date('now')
            """)

            stats["due_today"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM loans
                WHERE
                    status = 'ACTIVE'
                    AND due_date IS NOT NULL
                    AND due_date < date('now')
            """)

            stats["overdue"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM collateral
                WHERE status = 'HELD'
            """)

            stats["collateral_held"] = (
                cursor.fetchone()[0] or 0
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(amount),
                    0
                )
                FROM payments
                WHERE payment_date = date('now')
            """)

            stats["today_payments"] = (
                cursor.fetchone()[0] or 0
            )

        except Exception as error:

            print(
                "Dashboard database error:",
                error
            )

        finally:

            if connection:

                connection.close()

        return stats


    # ==================================================
    # BORROWERS
    # ==================================================

    def open_borrowers(self):

        try:

            BorrowerView(
                self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Borrowers Error",
                f"Unable to open Borrowers.\n\n{error}"
            )


    # ==================================================
    # LOANS
    # ==================================================

    def open_loans(self):

        try:

            LoanView(
                self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Loans Error",
                f"Unable to open Loans.\n\n{error}"
            )


    # ==================================================
    # PAYMENTS
    # ==================================================

    def open_payments(self):

        try:

            PaymentView(
                self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Payments Error",
                f"Unable to open Payments.\n\n{error}"
            )


    # ==================================================
    # PUSH FORWARD
    # ==================================================

    def open_push_forward(self):

        try:

            PushForwardView(
                self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Push Forward Error",
                f"Unable to open Push Forward.\n\n{error}"
            )


    # ==================================================
    # COLLATERAL
    # ==================================================

    def open_collateral(self):

        try:

            CollateralView(
                self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Collateral Error",
                f"Unable to open Collateral.\n\n{error}"
            )


    # ==================================================
    # EXCEL
    # ==================================================

    def open_excel(self):

        self.open_download_window()


    # ==================================================
    # ADMIN
    # ==================================================

    def open_admin(self):

        AdminWindow(
            self.root,
            self.show_dashboard
        )


# ======================================================
# ADMIN WINDOW
# ======================================================

class AdminWindow:

    def __init__(
        self,
        parent,
        refresh_callback
    ):

        self.parent = parent

        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "MikopoHub - Administrator"
        )

        self.window.geometry(
            "600x700"
        )

        self.window.resizable(
            False,
            False
        )

        self.build_interface()


    # ==================================================
    # BUILD ADMIN INTERFACE
    # ==================================================

    def build_interface(self):

        container = tk.Frame(
            self.window,
            padx=35,
            pady=30
        )

        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="🔐 Administrator",
            font=("Arial", 22, "bold")
        ).pack(
            pady=(0, 5)
        )

        tk.Label(
            container,
            text="Administrative Controls",
            font=("Arial", 11)
        ).pack(
            pady=(0, 20)
        )

        # ==================================================
        # CHANGE PASSWORD SECTION
        # ==================================================

        password_frame = tk.LabelFrame(
            container,
            text="Change Administrator Password",
            padx=20,
            pady=15
        )

        password_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        tk.Label(
            password_frame,
            text="Current Password"
        ).pack(
            anchor="w"
        )

        self.current_password_entry = tk.Entry(
            password_frame,
            show="*",
            font=("Arial", 11)
        )

        self.current_password_entry.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            password_frame,
            text="New Password"
        ).pack(
            anchor="w"
        )

        self.new_password_entry = tk.Entry(
            password_frame,
            show="*",
            font=("Arial", 11)
        )

        self.new_password_entry.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            password_frame,
            text="Confirm New Password"
        ).pack(
            anchor="w"
        )

        self.confirm_password_entry = tk.Entry(
            password_frame,
            show="*",
            font=("Arial", 11)
        )

        self.confirm_password_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Button(
            password_frame,
            text="CHANGE PASSWORD",
            font=("Arial", 10, "bold"),
            command=self.update_password
        ).pack(
            fill="x"
        )

        # ==================================================
        # DANGER ZONE
        # ==================================================

        danger_frame = tk.LabelFrame(
            container,
            text="Danger Zone",
            padx=20,
            pady=20
        )

        danger_frame.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            danger_frame,
            text="⚠️ RESET APPLICATION DATA",
            font=("Arial", 14, "bold")
        ).pack(
            pady=(0, 10)
        )

        tk.Label(
            danger_frame,
            text=(
                "This will permanently delete all "
                "borrowers, loans, payments, monthly "
                "periods, form fees, collateral and "
                "push forward history.\n\n"
                "The administrator password will NOT "
                "be deleted."
            ),
            justify="left",
            font=("Arial", 10)
        ).pack(
            pady=5
        )

        tk.Button(
            danger_frame,
            text="🗑 DELETE ALL DATA AND START AFRESH",
            font=("Arial", 11, "bold"),
            command=self.open_reset_window
        ).pack(
            fill="x",
            pady=(15, 5)
        )

        tk.Button(
            container,
            text="Close Admin",
            command=self.window.destroy
        ).pack(
            fill="x",
            pady=10
        )


    # ==================================================
    # CHANGE PASSWORD
    # ==================================================

    def update_password(self):

        current_password = (
            self.current_password_entry
            .get()
            .strip()
        )

        new_password = (
            self.new_password_entry
            .get()
            .strip()
        )

        confirm_password = (
            self.confirm_password_entry
            .get()
            .strip()
        )

        if not current_password:

            messagebox.showerror(
                "Password Required",
                "Enter your current password."
            )

            return

        if not new_password:

            messagebox.showerror(
                "Password Required",
                "Enter a new password."
            )

            return

        if new_password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                "The new passwords do not match."
            )

            return

        success, message = change_admin_password(
            current_password,
            new_password
        )

        if success:

            messagebox.showinfo(
                "Password Changed",
                message
            )

            self.current_password_entry.delete(
                0,
                tk.END
            )

            self.new_password_entry.delete(
                0,
                tk.END
            )

            self.confirm_password_entry.delete(
                0,
                tk.END
            )

        else:

            messagebox.showerror(
                "Password Change Failed",
                message
            )


    # ==================================================
    # OPEN RESET WINDOW
    # ==================================================

    def open_reset_window(self):

        reset_window = tk.Toplevel(
            self.window
        )

        reset_window.title(
            "Confirm Database Reset"
        )

        reset_window.geometry(
            "500x330"
        )

        reset_window.resizable(
            False,
            False
        )

        reset_window.transient(
            self.window
        )

        reset_window.grab_set()

        container = tk.Frame(
            reset_window,
            padx=30,
            pady=30
        )

        container.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            container,
            text="⚠️ DELETE EVERYTHING",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 15)
        )

        tk.Label(
            container,
            text=(
                "Enter the current administrator password "
                "to continue."
            ),
            justify="center"
        ).pack(
            pady=5
        )

        password_entry = tk.Entry(
            container,
            show="*",
            font=("Arial", 12)
        )

        password_entry.pack(
            fill="x",
            pady=15
        )

        password_entry.focus()


        def confirm_reset():

            password = (
                password_entry
                .get()
                .strip()
            )

            if not verify_admin_password(
                password
            ):

                messagebox.showerror(
                    "Access Denied",
                    "Incorrect administrator password."
                )

                password_entry.delete(
                    0,
                    tk.END
                )

                password_entry.focus()

                return

            confirmed = messagebox.askyesno(
                "⚠️ Delete Everything?",
                "WARNING!\n\n"
                "You are about to permanently delete "
                "ALL MikopoHub records.\n\n"
                "Do you want to continue?"
            )

            if not confirmed:

                return

            final_confirmed = messagebox.askyesno(
                "FINAL WARNING",
                "THIS IS THE FINAL CONFIRMATION.\n\n"
                "All borrowers, loans, payments, "
                "collateral and other application "
                "records will be permanently deleted.\n\n"
                "This cannot be undone.\n\n"
                "Do you really want to reset MikopoHub?"
            )

            if not final_confirmed:

                return

            success, message = reset_database()

            if success:

                reset_window.destroy()

                messagebox.showinfo(
                    "Reset Complete",
                    message
                )

                self.refresh_callback()

                self.window.destroy()

            else:

                messagebox.showerror(
                    "Reset Failed",
                    message
                )

        password_entry.bind(
            "<Return>",
            lambda event: confirm_reset()
        )

        tk.Button(
            container,
            text="🗑 DELETE ALL DATA",
            font=("Arial", 11, "bold"),
            command=confirm_reset
        ).pack(
            fill="x",
            pady=(10, 5)
        )

        tk.Button(
            container,
            text="Cancel",
            command=reset_window.destroy
        ).pack(
            fill="x",
            pady=5
        )


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":

    initialize_database()

    ensure_admin_settings()

    root = tk.Tk()

    app = MikopoHubApp(
        root
    )

    root.mainloop()