from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time

# ChaCha20 Benchmark
key = os.urandom(32)  # 256-bit key
nonce = os.urandom(16)  # Nonce
data = b"Sample plaintext" * 1024  # 16 KB data

# Encryption
start_time = time.time()
cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(data)
encryption_time = time.time() - start_time

print(f"ChaCha20 Encryption Time: {encryption_time:.6f}s")
