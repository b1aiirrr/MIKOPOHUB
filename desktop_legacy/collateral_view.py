import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_connection


class CollateralView:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)

        self.window.title(
            "MikopoHub - Collateral / Security"
        )

        self.window.geometry(
            "1200x700"
        )

        self.window.minsize(
            1000,
            600
        )

        self.selected_id = None

        self.build_interface()

        self.load_loans()

        self.load_collateral()

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
            padx=20,
            pady=15
        )

        tk.Label(
            header,
            text="Collateral / Security",
            font=("Arial", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Button(
            header,
            text="← Back to Dashboard",
            font=("Arial", 10),
            command=self.go_back
        ).pack(
            side="right"
        )

        # ----------------------------------------------
        # FORM
        # ----------------------------------------------

        form_frame = tk.LabelFrame(
            self.window,
            text="Collateral Details",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        form_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Loan

        tk.Label(
            form_frame,
            text="Loan:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.loan_var = tk.StringVar()

        self.loan_menu = ttk.Combobox(
            form_frame,
            textvariable=self.loan_var,
            state="readonly",
            width=40
        )

        self.loan_menu.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Security type

        tk.Label(
            form_frame,
            text="Security Type:"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.security_type_var = tk.StringVar()

        self.security_type_menu = ttk.Combobox(
            form_frame,
            textvariable=self.security_type_var,
            values=[
                "Motor Vehicle",
                "Motorcycle",
                "Land",
                "House",
                "Electronics",
                "Phone",
                "Laptop",
                "Furniture",
                "Business Equipment",
                "Jewelry",
                "Other"
            ],
            width=25
        )

        self.security_type_menu.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # Description

        tk.Label(
            form_frame,
            text="Description:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.description_entry = tk.Entry(
            form_frame,
            width=43
        )

        self.description_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Estimated value

        tk.Label(
            form_frame,
            text="Estimated Value:"
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.value_entry = tk.Entry(
            form_frame,
            width=28
        )

        self.value_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        # Serial number

        tk.Label(
            form_frame,
            text="Serial / Registration No.:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.serial_entry = tk.Entry(
            form_frame,
            width=43
        )

        self.serial_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # Condition

        tk.Label(
            form_frame,
            text="Condition:"
        ).grid(
            row=2,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.condition_var = tk.StringVar()

        self.condition_menu = ttk.Combobox(
            form_frame,
            textvariable=self.condition_var,
            values=[
                "New",
                "Good",
                "Fair",
                "Poor"
            ],
            width=25
        )

        self.condition_menu.grid(
            row=2,
            column=3,
            padx=5,
            pady=5
        )

        # Date received

        tk.Label(
            form_frame,
            text="Date Received:"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.date_entry = tk.Entry(
            form_frame,
            width=43
        )

        self.date_entry.grid(
            row=3,
            column=1,
            padx=5,
            pady=5
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Status

        tk.Label(
            form_frame,
            text="Status:"
        ).grid(
            row=3,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.status_var = tk.StringVar(
            value="HELD"
        )

        self.status_menu = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=[
                "HELD",
                "RELEASED",
                "SOLD",
                "RETURNED"
            ],
            state="readonly",
            width=25
        )

        self.status_menu.grid(
            row=3,
            column=3,
            padx=5,
            pady=5
        )

        # Notes

        tk.Label(
            form_frame,
            text="Notes:"
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.notes_entry = tk.Entry(
            form_frame,
            width=43
        )

        self.notes_entry.grid(
            row=4,
            column=1,
            padx=5,
            pady=5
        )

        # ----------------------------------------------
        # BUTTONS
        # ----------------------------------------------

        button_frame = tk.Frame(
            form_frame
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=4,
            pady=15
        )

        tk.Button(
            button_frame,
            text="➕ Add Collateral",
            width=18,
            command=self.add_collateral
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="✏ Edit",
            width=15,
            command=self.edit_collateral
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="🗑 Delete",
            width=15,
            command=self.delete_collateral
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------
        # SEARCH
        # ----------------------------------------------

        search_frame = tk.Frame(
            self.window
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )

        search_entry.pack(
            side="left",
            padx=10
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_collateral()
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
            padx=20,
            pady=5
        )

        columns = (
            "id",
            "collateral_number",
            "loan",
            "security_type",
            "description",
            "value",
            "serial",
            "condition",
            "date_received",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "collateral_number": "Collateral No.",
            "loan": "Loan",
            "security_type": "Security Type",
            "description": "Description",
            "value": "Estimated Value",
            "serial": "Serial / Reg. No.",
            "condition": "Condition",
            "date_received": "Date Received",
            "status": "Status"
        }

        widths = {
            "id": 50,
            "collateral_number": 110,
            "loan": 100,
            "security_type": 120,
            "description": 180,
            "value": 110,
            "serial": 130,
            "condition": 80,
            "date_received": 110,
            "status": 90
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_collateral
        )

    # ==================================================
    # LOAD LOANS
    # ==================================================

    def load_loans(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                loan_number,
                principal
            FROM loans
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        self.loan_map = {}

        values = []

        for row in rows:

            display = (
                f"{row['loan_number']} - "
                f"KSh {row['principal']:,.2f}"
            )

            values.append(display)

            self.loan_map[display] = row["id"]

        self.loan_menu["values"] = values

    # ==================================================
    # LOAD COLLATERAL
    # ==================================================

    def load_collateral(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        search = self.search_var.get().strip()

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            SELECT
                c.id,
                c.collateral_number,
                l.loan_number,
                c.security_type,
                c.description,
                c.estimated_value,
                c.serial_number,
                c.condition,
                c.date_received,
                c.status
            FROM collateral c
            INNER JOIN loans l
                ON c.loan_id = l.id
        """

        parameters = []

        if search:

            query += """
                WHERE
                    c.collateral_number LIKE ?
                    OR l.loan_number LIKE ?
                    OR c.security_type LIKE ?
                    OR c.description LIKE ?
                    OR c.serial_number LIKE ?
                    OR c.status LIKE ?
            """

            search_value = f"%{search}%"

            parameters = [
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ]

        query += """
            ORDER BY c.id DESC
        """

        cursor.execute(
            query,
            parameters
        )

        rows = cursor.fetchall()

        connection.close()

        for row in rows:

            value = row["estimated_value"]

            if value is not None:
                value = f"KSh {value:,.2f}"
            else:
                value = ""

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["collateral_number"],
                    row["loan_number"],
                    row["security_type"],
                    row["description"],
                    value,
                    row["serial_number"] or "",
                    row["condition"] or "",
                    row["date_received"] or "",
                    row["status"]
                )
            )

    # ==================================================
    # SELECT COLLATERAL
    # ==================================================

    def select_collateral(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        if not values:
            return

        self.selected_id = int(
            values[0]
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM collateral
            WHERE id = ?
        """, (
            self.selected_id,
        ))

        row = cursor.fetchone()

        connection.close()

        if not row:
            return

        self.clear_form(
            keep_selection=True
        )

        # Find loan

        for display, loan_id in self.loan_map.items():

            if loan_id == row["loan_id"]:

                self.loan_var.set(
                    display
                )

                break

        self.security_type_var.set(
            row["security_type"] or ""
        )

        self.description_entry.insert(
            0,
            row["description"] or ""
        )

        if row["estimated_value"] is not None:

            self.value_entry.insert(
                0,
                str(row["estimated_value"])
            )

        self.serial_entry.insert(
            0,
            row["serial_number"] or ""
        )

        self.condition_var.set(
            row["condition"] or ""
        )

        self.date_entry.insert(
            0,
            row["date_received"] or ""
        )

        self.status_var.set(
            row["status"] or "HELD"
        )

        self.notes_entry.insert(
            0,
            row["notes"] or ""
        )

    # ==================================================
    # ADD COLLATERAL
    # ==================================================

    def add_collateral(self):

        loan_display = self.loan_var.get().strip()

        security_type = (
            self.security_type_var.get().strip()
        )

        description = (
            self.description_entry.get().strip()
        )

        value_text = (
            self.value_entry.get().strip()
        )

        serial_number = (
            self.serial_entry.get().strip()
        )

        condition = (
            self.condition_var.get().strip()
        )

        date_received = (
            self.date_entry.get().strip()
        )

        status = (
            self.status_var.get().strip()
        )

        notes = (
            self.notes_entry.get().strip()
        )

        if not loan_display:

            messagebox.showwarning(
                "Missing Information",
                "Please select a loan."
            )

            return

        if not security_type:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the security type."
            )

            return

        if not description:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a description."
            )

            return

        loan_id = self.loan_map.get(
            loan_display
        )

        if not loan_id:

            messagebox.showerror(
                "Error",
                "Invalid loan selected."
            )

            return

        estimated_value = None

        if value_text:

            try:

                estimated_value = float(
                    value_text.replace(
                        ",",
                        ""
                    )
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Value",
                    "Estimated value must be a valid number."
                )

                return

        connection = get_connection()

        cursor = connection.cursor()

        # Generate collateral number

        cursor.execute("""
            SELECT COUNT(*)
            FROM collateral
        """)

        count = cursor.fetchone()[0] + 1

        collateral_number = (
            f"COL-{count:04d}"
        )

        try:

            cursor.execute("""
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
            """, (
                collateral_number,
                loan_id,
                security_type,
                description,
                estimated_value,
                serial_number or None,
                condition or None,
                date_received or None,
                status or "HELD",
                notes or None
            ))

            connection.commit()

            connection.close()

            messagebox.showinfo(
                "Success",
                f"Collateral {collateral_number} added successfully."
            )

            self.clear_form()

            self.load_collateral()

        except Exception as error:

            connection.rollback()

            connection.close()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==================================================
    # EDIT COLLATERAL
    # ==================================================

    def edit_collateral(self):

        if not self.selected_id:

            messagebox.showwarning(
                "No Selection",
                "Please select collateral to edit."
            )

            return

        loan_display = self.loan_var.get().strip()

        security_type = (
            self.security_type_var.get().strip()
        )

        description = (
            self.description_entry.get().strip()
        )

        value_text = (
            self.value_entry.get().strip()
        )

        serial_number = (
            self.serial_entry.get().strip()
        )

        condition = (
            self.condition_var.get().strip()
        )

        date_received = (
            self.date_entry.get().strip()
        )

        status = (
            self.status_var.get().strip()
        )

        notes = (
            self.notes_entry.get().strip()
        )

        if not loan_display or not security_type or not description:

            messagebox.showwarning(
                "Missing Information",
                "Loan, security type and description are required."
            )

            return

        loan_id = self.loan_map.get(
            loan_display
        )

        if not loan_id:
            return

        estimated_value = None

        if value_text:

            try:

                estimated_value = float(
                    value_text.replace(
                        ",",
                        ""
                    )
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Value",
                    "Estimated value must be a valid number."
                )

                return

        confirm = messagebox.askyesno(
            "Confirm Edit",
            "Are you sure you want to update this collateral record?"
        )

        if not confirm:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                UPDATE collateral
                SET
                    loan_id = ?,
                    security_type = ?,
                    description = ?,
                    estimated_value = ?,
                    serial_number = ?,
                    condition = ?,
                    date_received = ?,
                    status = ?,
                    notes = ?
                WHERE id = ?
            """, (
                loan_id,
                security_type,
                description,
                estimated_value,
                serial_number or None,
                condition or None,
                date_received or None,
                status or "HELD",
                notes or None,
                self.selected_id
            ))

            connection.commit()

            connection.close()

            messagebox.showinfo(
                "Updated",
                "Collateral record updated successfully."
            )

            self.clear_form()

            self.load_collateral()

        except Exception as error:

            connection.rollback()

            connection.close()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==================================================
    # DELETE COLLATERAL
    # ==================================================

    def delete_collateral(self):

        if not self.selected_id:

            messagebox.showwarning(
                "No Selection",
                "Please select collateral to delete."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this collateral record?"
        )

        if not confirm:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                DELETE FROM collateral
                WHERE id = ?
            """, (
                self.selected_id,
            ))

            connection.commit()

            connection.close()

            messagebox.showinfo(
                "Deleted",
                "Collateral record deleted successfully."
            )

            self.clear_form()

            self.load_collateral()

        except Exception as error:

            connection.rollback()

            connection.close()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # ==================================================
    # CLEAR FORM
    # ==================================================

    def clear_form(self, keep_selection=False):

        if not keep_selection:

            self.selected_id = None

        self.loan_var.set("")

        self.security_type_var.set("")

        self.description_entry.delete(
            0,
            tk.END
        )

        self.value_entry.delete(
            0,
            tk.END
        )

        self.serial_entry.delete(
            0,
            tk.END
        )

        self.condition_var.set("")

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.status_var.set(
            "HELD"
        )

        self.notes_entry.delete(
            0,
            tk.END
        )

    # ==================================================
    # BACK TO DASHBOARD
    # ==================================================

    def go_back(self):

        self.window.destroy()


# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    CollateralView(
        root
    )

    root.mainloop()