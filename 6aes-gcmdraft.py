from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import time

key = os.urandom(32)
iv = os.urandom(12)
data = b"Sample plaintext" * 1024  # 16 KB data

# Encryption
cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
encryptor = cipher.encryptor()
start_time = time.time()
ciphertext = encryptor.update(data) + encryptor.finalize()
encryption_time = time.time() - start_time
print(f"AES-GCM Encryption Time: {encryption_time:.6f}s")
