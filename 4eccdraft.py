from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import time

# Key Generation
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Data to Sign
data = b"Sample plaintext"

# Signing
start_time = time.time()
signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
signing_time = time.time() - start_time

# Verifying
start_time = time.time()
public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
verification_time = time.time() - start_time

print(f"ECC Signing Time: {signing_time:.6f}s")
print(f"ECC Verification Time: {verification_time:.6f}s")
