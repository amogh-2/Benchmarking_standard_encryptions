from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import time

# AES Benchmark
key = b'\x00' * 16  # 128-bit key
iv = b'\x00' * 16   # Initialization vector
data = b"Sample plaintext" * 1024  # 16 KB data

# Encryption
start_time = time.time()
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(data) + encryptor.finalize()
encryption_time = time.time() - start_time

# Decryption
start_time = time.time()
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()
decryption_time = time.time() - start_time

print(f"AES Encryption Time: {encryption_time:.6f}s")
print(f"AES Decryption Time: {decryption_time:.6f}s")
