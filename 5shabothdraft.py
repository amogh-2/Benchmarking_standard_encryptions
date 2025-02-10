from cryptography.hazmat.primitives import hashes
import time

# Data to Hash
data = b"Sample plaintext" * 1024  # 16 KB data

# SHA-256
digest = hashes.Hash(hashes.SHA256())
start_time = time.time()
digest.update(data)
hash_value = digest.finalize()
hash_time = time.time() - start_time
print(f"SHA-256 Hashing Time: {hash_time:.6f}s")

# SHA-3
digest = hashes.Hash(hashes.SHA3_256())
start_time = time.time()
digest.update(data)
hash_value = digest.finalize()
hash_time = time.time() - start_time
print(f"SHA-3 Hashing Time: {hash_time:.6f}s")
