from pwdlib import PasswordHash


# Wird für das sichere Hashen und Prüfen von Passwörtern verwendet
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)