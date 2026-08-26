from database import get_connection, initialize_database
from admin_service import (
    ensure_admin_settings,
    verify_admin_password
)

import getpass


# ======================================================
# RESET DATABASE
# ======================================================

def reset_database():

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "PRAGMA foreign_keys = OFF"
        )

        tables = [
            "push_forward_history",
            "payments",
            "monthly_periods",
            "collateral",
            "form_fees",
            "loans",
            "borrowers"
        ]

        for table in tables:

            cursor.execute(
                f"DELETE FROM {table}"
            )

        # Reset automatic ID counters safely

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'sqlite_sequence'
        """)

        sequence_table = cursor.fetchone()

        if sequence_table:

            cursor.execute(
                "DELETE FROM sqlite_sequence"
            )

        connection.commit()

        return True, (
            "All MikopoHub data has been deleted successfully.\n\n"
            "The application is now ready for a fresh start."
        )

    except Exception as error:

        if connection:

            connection.rollback()

        return False, str(error)

    finally:

        if connection:

            connection.close()

        initialize_database()


# ======================================================
# MANUAL RESET
# ======================================================

def run_manual_reset():

    ensure_admin_settings()

    print("\n" + "=" * 55)
    print("       MIKOPOHUB DATABASE RESET")
    print("=" * 55)

    print(
        "\nWARNING: This will permanently "
        "delete ALL application data."
    )

    password = getpass.getpass(
        "\nEnter Admin Password: "
    )

    # Uses the SAME password as the dashboard

    if not verify_admin_password(
        password
    ):

        print(
            "\nACCESS DENIED!"
        )

        print(
            "Incorrect admin password."
        )

        return

    confirmation = input(
        "\nType DELETE EVERYTHING to continue: "
    ).strip()

    if confirmation != "DELETE EVERYTHING":

        print(
            "\nDatabase reset cancelled."
        )

        return

    success, message = reset_database()

    if success:

        print(
            "\nRESET SUCCESSFUL"
        )

        print(message)

    else:

        print(
            "\nRESET FAILED"
        )

        print(message)


# ======================================================
# START MANUAL RESET
# ======================================================

if __name__ == "__main__":

    run_manual_reset()