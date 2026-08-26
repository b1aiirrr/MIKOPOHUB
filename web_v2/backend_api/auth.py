import bcrypt

# Legacy plain text password for reference: "MikopoHubAdmin2026"
LEGACY_PLAIN_PASSWORD = "MikopoHubAdmin2026"


def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt with a generated salt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a bcrypt hash string."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# Pre-computed bcrypt hash for admin credential validation
ADMIN_PASSWORD_HASH = hash_password(LEGACY_PLAIN_PASSWORD)
