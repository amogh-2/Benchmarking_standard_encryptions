import os
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_file(input_file, output_file, key):
    """ Encrypt file using AES-GCM """
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_file, "rb") as f:
        plaintext = f.read()
    
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(iv + encryptor.tag + ciphertext)

    return iv, encryptor.tag, ciphertext

def decrypt_file(encrypted_file, decrypted_file, key):
    """ Decrypt AES-GCM encrypted file """
    with open(encrypted_file, "rb") as f:
        data = f.read()

    iv, tag, ciphertext = data[:12], data[12:28], data[28:]

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(decrypted_file, "wb") as f:
        f.write(plaintext)
    
    return np.frombuffer(plaintext, dtype=np.uint8), np.frombuffer(ciphertext, dtype=np.uint8)  # Convert to NumPy arrays

def calculate_correlation(data1, data2):
    """ Calculate correlation coefficient between two byte sequences """
    if len(data1) != len(data2):
        min_length = min(len(data1), len(data2))
        data1, data2 = data1[:min_length], data2[:min_length]  # Trim to match lengths

    if len(data1) == 0 or len(data2) == 0:
        return 0  # Handle empty file case

    correlation = np.corrcoef(data1, data2)[0, 1]
    return correlation

# User input for file paths
input_file = input("Enter the input file path: ")
encrypted_file = "encrypted_file.bin"
decrypted_file = "decrypted_output.txt"
key = os.urandom(32)  # 256-bit AES key

# Encrypt File
iv, tag, ciphertext = encrypt_file(input_file, encrypted_file, key)

# Decrypt File
decrypted_content, cipher_values = decrypt_file(encrypted_file, decrypted_file, key)

# Read original file data as a NumPy array
with open(input_file, "rb") as f:
    orig_data = np.frombuffer(f.read(), dtype=np.uint8)

# Calculate correlation coefficients
correlation_original_decrypted = calculate_correlation(orig_data, decrypted_content)
correlation_original_ciphertext = calculate_correlation(orig_data, cipher_values)

# Results
print("\nEncryption and decryption complete.")
print("Encrypted File:", encrypted_file)
print("Decrypted File:", decrypted_file)
print("\nCorrelation Coefficient (Original ↔ Decrypted):", correlation_original_decrypted)
print("Correlation Coefficient (Original ↔ Ciphertext):", correlation_original_ciphertext)
