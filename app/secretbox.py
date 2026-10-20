"""Encryption for secrets kept in the database (the CCS+ password, Google's client secret and
sign-in), and hashing for the status-page password.

Encrypted values use a key derived from DB_PASSWORD, which is not stored in the database, so a
copy of the database alone can't be used to read them.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ROUNDS = 390_000          # PBKDF2-SHA256 rounds for the encryption key
SCRYPT = {"n": 2 ** 14, "r": 8, "p": 1}   # status-page password hashing (about 50 ms)


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


class SecretBox:
    def __init__(self, key_secret: str):
        self._key_secret = key_secret
        self._keys: dict[bytes, Fernet] = {}    # salt -> key (deriving one is slow on purpose)

    def _fernet(self, salt: bytes) -> Fernet:
        if not self._key_secret:
            raise ValueError("DB_PASSWORD is needed to store secrets securely.")
        if salt not in self._keys:
            if len(self._keys) >= 8:
                self._keys.clear()
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ROUNDS)
            self._keys[salt] = Fernet(base64.urlsafe_b64encode(kdf.derive(self._key_secret.encode())))
        return self._keys[salt]

    def seal(self, text: str) -> dict:
        """Encrypt with a key derived from DB_PASSWORD and a fresh salt."""
        salt = secrets.token_bytes(16)
        return {"v": 1, "salt": _b64(salt), "token": self._fernet(salt).encrypt(text.encode()).decode()}

    def unseal(self, sealed: dict) -> str:
        """Decrypt a value from seal(). Raises ValueError if it can't be read (e.g. DB_PASSWORD changed)."""
        try:
            return self._fernet(_unb64(sealed["salt"])).decrypt(sealed["token"].encode()).decode()
        except (InvalidToken, KeyError, ValueError, TypeError) as e:
            raise ValueError("can't be decrypted") from e


def hash_password(password: str) -> dict:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, dklen=32, **SCRYPT)
    return {"alg": "scrypt", **SCRYPT, "salt": _b64(salt), "hash": _b64(digest)}


def check_password(password: str, stored: dict) -> bool:
    try:
        digest = hashlib.scrypt(password.encode(), salt=_unb64(stored["salt"]), dklen=32,
                                n=stored["n"], r=stored["r"], p=stored["p"])
        return hmac.compare_digest(digest, _unb64(stored["hash"]))
    except (KeyError, ValueError, TypeError):
        return False
