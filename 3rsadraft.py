from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import time

# Key Generation
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Data to Encrypt
data = b"Sample plaintext" * 1024  # 16 KB data

# Encryption
start_time = time.time()
ciphertext = public_key.encrypt(
    data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
encryption_time = time.time() - start_time

# Decryption
start_time = time.time()
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
decryption_time = time.time() - start_time

print(f"RSA Encryption Time: {encryption_time:.6f}s")
print(f"RSA Decryption Time: {decryption_time:.6f}s")
