import os
import sys
from cryptography.fernet import Fernet, InvalidToken

def get_key():
    key = os.environ.get("FERNET_KEY")
    if not key:
        sys.exit("Erreur : FERNET_KEY absente (configurer le Secret GitHub).")
    return key.encode()

def encrypt_file(src, dst):
    f = Fernet(get_key())
    with open(src, "rb") as fp:
        data = fp.read()
    with open(dst, "wb") as fp:
        fp.write(f.encrypt(data))
    print(f"Chiffré : {src} -> {dst}")

def decrypt_file(src, dst):
    f = Fernet(get_key())
    with open(src, "rb") as fp:
        token = fp.read()
    try:
        data = f.decrypt(token)
    except InvalidToken:
        sys.exit("Erreur : token invalide ou clé incorrecte.")
    with open(dst, "wb") as fp:
        fp.write(data)
    print(f"Déchiffré : {src} -> {dst}")

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("encrypt", "decrypt"):
        sys.exit("Usage : python app/fernet_atelier1.py encrypt|decrypt <source> <destination>")
    action, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    (encrypt_file if action == "encrypt" else decrypt_file)(src, dst)