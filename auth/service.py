from auth.password import hash_password, verify_password
from db.users_repo import create_user, get_user_by_username


def ensure_default_users():
    if get_user_by_username("student") is None:
        create_user("student", hash_password("student123"), "student")
    if get_user_by_username("reviewer") is None:
        create_user("reviewer", hash_password("reviewer123"), "reviewer")


def authenticate(username, password):
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user
