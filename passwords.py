import hashlib
import hmac
import secrets

# Passwords are hashed with PBKDF2 using SHA-256. PBKDF2 runs SHA-256
# many times over the salted password, which makes guessing passwords
# from a stolen database far slower than a single SHA-256 hash.
ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16

MIN_PASSWORD_LENGTH = 8


def hash_password(password):
    """
    Returns a string holding the algorithm, iteration count, salt
    and hash, so the password can be checked later.
    """
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )

    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password, stored_hash):
    try:
        algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
        if algorithm != ALGORITHM:
            return False

        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations)
        )
    except (AttributeError, ValueError):
        return False

    # compare_digest takes the same time whether or not the hashes match
    return hmac.compare_digest(digest.hex(), digest_hex)


def validate_new_password(password):
    """
    Returns an error message, or None if the password is acceptable.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return (
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
        )

    return None
