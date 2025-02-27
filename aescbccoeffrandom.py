import os
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pad(data):
    """Pad data to be multiple of AES block size (16 bytes)"""
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    """Remove padding from data"""
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_aes_cbc(key, iv, plaintext):
    """Encrypt plaintext using AES-CBC"""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(pad(plaintext)) + encryptor.finalize()
    return ciphertext

def decrypt_aes_cbc(key, iv, ciphertext):
    """Decrypt ciphertext using AES-CBC"""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(decrypted_padded)

def correlation_coefficient(data1, data2):
    """Compute correlation coefficient for equal-sized inputs"""
    min_length = min(len(data1), len(data2))  # Ensure same length
    values1 = np.frombuffer(data1[:min_length], dtype=np.uint8)
    values2 = np.frombuffer(data2[:min_length], dtype=np.uint8)
    return np.corrcoef(values1, values2)[0, 1]

# User input
user_input = input("Enter a random string: ").encode()

# Generate a 256-bit key and 16-byte IV
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # AES block size IV

# Encrypt and decrypt
ciphertext = encrypt_aes_cbc(key, iv, user_input)
decrypted_text = decrypt_aes_cbc(key, iv, ciphertext)

# Calculate correlation coefficient
corr_decrypt = correlation_coefficient(user_input, decrypted_text)  # Should be ~1
corr_encrypt = correlation_coefficient(user_input, ciphertext)  # Should be ~0

# Output results
print("\nOriginal Text: ", user_input.decode())
print("Decrypted Text: ", decrypted_text.decode())
print("Correlation Coefficient (Original vs. Decrypted): ", corr_decrypt)
print("Correlation Coefficient (Original vs. Ciphertext): ", corr_encrypt)
