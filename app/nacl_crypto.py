import os
import sys
import nacl.secret
import nacl.utils
from nacl.exceptions import CryptoError

KEY_FILE = "nacl.key"

def generate_key():
    if os.path.exists(KEY_FILE):
        sys.exit(f"Erreur : {KEY_FILE} existe déjà.")
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"Clé générée dans {KEY_FILE}")

def load_key():
    if not os.path.exists(KEY_FILE):
        sys.exit(f"Erreur : {KEY_FILE} manquant. Lancer 'generate-key' d'abord.")
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file(src, dst):
    box = nacl.secret.SecretBox(load_key())
    with open(src, "rb") as f:
        data = f.read()
    encrypted = box.encrypt(data)
    with open(dst, "wb") as f:
        f.write(encrypted)
    print(f"Chiffré : {src} -> {dst}")

def decrypt_file(src, dst):
    box = nacl.secret.SecretBox(load_key())
    with open(src, "rb") as f:
        token = f.read()
    try:
        data = box.decrypt(token)
    except CryptoError:
        sys.exit("Erreur : fichier altéré ou clé incorrecte.")
    with open(dst, "wb") as f:
        f.write(data)
    print(f"Déchiffré : {src} -> {dst}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage :\n  generate-key\n  encrypt <src> <dst>\n  decrypt <src> <dst>")
    cmd = sys.argv[1]
    if cmd == "generate-key":
        generate_key()
    elif cmd == "encrypt" and len(sys.argv) == 4:
        encrypt_file(sys.argv[2], sys.argv[3])
    elif cmd == "decrypt" and len(sys.argv) == 4:
        decrypt_file(sys.argv[2], sys.argv[3])
    else:
        sys.exit("Commande invalide.")