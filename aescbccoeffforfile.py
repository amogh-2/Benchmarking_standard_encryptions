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

def encrypt_file(input_filename, output_filename, key, iv):
    """Encrypts a file using AES-CBC"""
    with open(input_filename, 'rb') as f:
        plaintext = f.read()
    ciphertext = encrypt_aes_cbc(key, iv, plaintext)
    with open(output_filename, 'wb') as f:
        f.write(ciphertext)
    return plaintext, ciphertext

def decrypt_file(input_filename, output_filename, key, iv):
    """Decrypts a file using AES-CBC"""
    with open(input_filename, 'rb') as f:
        ciphertext = f.read()
    decrypted_text = decrypt_aes_cbc(key, iv, ciphertext)
    with open(output_filename, 'wb') as f:
        f.write(decrypted_text)
    return decrypted_text

# User input for filenames
input_filename = input("Enter input file path: ")
encrypted_filename = "encrypted_file.bin"
decrypted_filename = "decrypted_file.txt"

# Generate a 256-bit key and 16-byte IV
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # AES block size IV

# Encrypt & decrypt the file
original_data, encrypted_data = encrypt_file(input_filename, encrypted_filename, key, iv)
decrypted_data = decrypt_file(encrypted_filename, decrypted_filename, key, iv)

# Calculate correlation coefficient
corr_decrypt = correlation_coefficient(original_data, decrypted_data)  # Should be ~1
corr_encrypt = correlation_coefficient(original_data, encrypted_data)  # Should be ~0

# Output results
print("\nEncryption and Decryption completed.")
print("Correlation Coefficient (Original vs. Decrypted): ", corr_decrypt)
print("Correlation Coefficient (Original vs. Ciphertext): ", corr_encrypt)
