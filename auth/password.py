import hashlib

try:
    import bcrypt
except Exception:  # pragma: no cover
    bcrypt = None


def hash_password(password):
    if bcrypt:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return f"sha256${digest}"


def verify_password(password, stored_hash):
    if stored_hash.startswith("sha256$"):
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return stored_hash == f"sha256${digest}"
    if bcrypt:
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    return False
