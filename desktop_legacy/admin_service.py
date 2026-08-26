from database import get_connection


DEFAULT_ADMIN_PASSWORD = "MikopoHubAdmin2026"


def ensure_admin_settings():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            admin_password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        SELECT admin_password
        FROM admin_settings
        WHERE id = 1
    """)

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO admin_settings (
                id,
                admin_password
            )
            VALUES (?, ?)
        """, (
            1,
            DEFAULT_ADMIN_PASSWORD
        ))

    connection.commit()
    connection.close()


def verify_admin_password(password):

    ensure_admin_settings()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT admin_password
        FROM admin_settings
        WHERE id = 1
    """)

    admin = cursor.fetchone()

    connection.close()

    if admin is None:
        return False

    return password == admin["admin_password"]


def change_admin_password(
    current_password,
    new_password
):

    if not current_password:

        return False, (
            "Please enter the current password."
        )

    if not new_password:

        return False, (
            "Please enter a new password."
        )

    if len(new_password) < 6:

        return False, (
            "The new password must contain "
            "at least 6 characters."
        )

    # Verify current password first

    if not verify_admin_password(
        current_password
    ):

        return False, (
            "The current admin password is incorrect."
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE admin_settings

        SET admin_password = ?

        WHERE id = 1
    """, (
        new_password,
    ))

    connection.commit()
    connection.close()

    return True, (
        "Admin password changed successfully."
    )