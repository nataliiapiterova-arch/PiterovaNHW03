import hashlib
import os
import secrets
import time

from . import models, tokens
from .database import DATA_DIR

PBKDF2_ITERATIONS = 200_000
SESSION_COOKIE_NAME = "session"
SESSION_TTL_SECONDS = 7 * 24 * 3600

_SECRET_KEY_PATH = os.path.join(DATA_DIR, "secret.key")


def get_secret_key():
    """Loads (or generates on first run) a random signing key persisted to disk.

    Kept out of source control so a real deployment doesn't ship a shared secret.
    """
    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        return env_key
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(_SECRET_KEY_PATH):
        with open(_SECRET_KEY_PATH, "w") as f:
            f.write(secrets.token_hex(32))
    with open(_SECRET_KEY_PATH) as f:
        return f.read().strip()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS
    )
    return digest.hex(), salt


def verify_password(password, password_hash, salt):
    candidate, _ = hash_password(password, salt)
    return secrets.compare_digest(candidate, password_hash)


def signup(email, password):
    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("Enter a valid email address.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if models.get_user_by_email(email):
        raise ValueError("An account with that email already exists.")
    password_hash, salt = hash_password(password)
    user_id = models.create_user(email, password_hash, salt)
    return user_id


def login(email, password):
    email = email.strip().lower()
    user = models.get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"], user["salt"]):
        raise ValueError("Invalid email or password.")
    return user


def create_session_token(user_id):
    payload = {
        "sub": user_id,
        "csrf": secrets.token_hex(16),
        "iat": int(time.time()),
        "exp": int(time.time()) + SESSION_TTL_SECONDS,
    }
    return tokens.sign(payload, get_secret_key())


def decode_session_token(token):
    return tokens.verify(token, get_secret_key())


def current_user_from_cookie(cookie_value):
    if not cookie_value:
        return None, None
    payload = decode_session_token(cookie_value)
    if not payload:
        return None, None
    user = models.get_user_by_id(payload["sub"])
    return user, payload.get("csrf")
