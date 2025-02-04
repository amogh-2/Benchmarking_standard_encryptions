import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Function to benchmark AES-CBC encryption
def benchmark_aes_cbc(data_size_kb, key_size_bits=128):
    # Generate random data
    data = os.urandom(data_size_kb * 1024)
    key = os.urandom(key_size_bits // 8)
    iv = os.urandom(16)  # 16 bytes for AES-CBC

    # Initialize AES-CBC cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Benchmark encryption
    start_time = time.perf_counter()
    ciphertext = encryptor.update(data) + encryptor.finalize()  # noqa: F841
    end_time = time.perf_counter()

    # Results
    encryption_time = end_time - start_time
    print(f"Encryption Time: {encryption_time:.6f} seconds")
    return encryption_time

# Run the benchmark with 16KB of data
data_size_kb = 16
benchmark_aes_cbc(data_size_kb)
