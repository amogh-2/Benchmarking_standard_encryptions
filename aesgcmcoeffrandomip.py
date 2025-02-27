import os
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_aes_gcm(plaintext, key):
    """ Encrypt plaintext using AES-GCM """
    iv = os.urandom(12)  # 12-byte IV for AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, encryptor.tag, ciphertext

def decrypt_aes_gcm(iv, tag, ciphertext, key):
    """ Decrypt ciphertext using AES-GCM """
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def calculate_correlation(data1, data2):
    """ Calculate correlation coefficient between two sets of values """
    if len(data1) != len(data2):
        min_length = min(len(data1), len(data2))
        data1, data2 = data1[:min_length], data2[:min_length]  # Trim to match lengths

    correlation = np.corrcoef(data1, data2)[0, 1]
    return correlation

# User input
user_input = input("Enter a random text: ")
key = os.urandom(32)  # 256-bit AES key

# Encryption
iv, tag, ciphertext = encrypt_aes_gcm(user_input, key)

# Decryption
decrypted_text = decrypt_aes_gcm(iv, tag, ciphertext, key)

# Convert data to numeric values for correlation calculation
orig_values = np.array([ord(c) for c in user_input])   # ASCII values of original text
dec_values = np.array([ord(c) for c in decrypted_text])  # ASCII values of decrypted text
cipher_values = np.frombuffer(ciphertext, dtype=np.uint8)  # Byte values of ciphertext

# Correlation Coefficients
correlation_original_decrypted = calculate_correlation(orig_values, dec_values)
correlation_original_ciphertext = calculate_correlation(orig_values, cipher_values)

# Results
print("\nOriginal Text:", user_input)
print("Decrypted Text:", decrypted_text)
print("\nCorrelation Coefficient (Original ↔ Decrypted):", correlation_original_decrypted)
print("Correlation Coefficient (Original ↔ Ciphertext):", correlation_original_ciphertext)

