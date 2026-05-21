import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import logging

logging.basicConfig(level=logging.INFO)

class AESManager:
    def __init__(self, key=None):
        if key is None:
            # Generate a random 32-byte key for AES-256
            self.key = os.urandom(32)
        else:
            self.key = key if isinstance(key, bytes) else key.encode()
            if len(self.key) != 32:
                raise ValueError("Key must be 32 bytes for AES-256")

    def encrypt_file(self, file_path):
        """Encrypts a file and appends .crypt extension."""
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return False

        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            with open(file_path, 'rb') as f:
                data = f.read()

            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            with open(file_path + ".crypt", 'wb') as f:
                f.write(iv + encrypted_data)
            
            # Optionally delete original file
            # os.remove(file_path)
            logging.info(f"Encrypted: {file_path} -> {file_path}.crypt")
            return True
        except Exception as e:
            logging.error(f"Encryption failed for {file_path}: {e}")
            return False

    def decrypt_file(self, encrypted_file_path):
        """Decrypts a .crypt file."""
        if not encrypted_file_path.endswith(".crypt"):
            logging.error("Not a .crypt file")
            return False

        try:
            with open(encrypted_file_path, 'rb') as f:
                data = f.read()

            iv = data[:16]
            encrypted_content = data[16:]

            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            decrypted_padded_data = decryptor.update(encrypted_content) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            original_path = encrypted_file_path.replace(".crypt", "")
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            logging.info(f"Decrypted: {encrypted_file_path} -> {original_path}")
            return True
        except Exception as e:
            logging.error(f"Decryption failed for {encrypted_file_path}: {e}")
            return False

if __name__ == "__main__":
    # Example usage:
    # manager = AESManager()
    # manager.encrypt_file("test.txt")
    pass
