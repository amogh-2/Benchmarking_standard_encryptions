import os
import secrets
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def xor_bytes(a, b):
    """Returns the number of differing bits between two byte sequences."""
    return sum(bin(x ^ y).count('1') for x, y in zip(a, b))

def compute_avalanche_effect(original_text, modified_text, key, iv):
    """Computes the avalanche effect between two AES CBC encrypted texts."""
    backend = default_backend()
    
    # Encrypt the original text
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    original_ciphertext = encryptor.update(original_text) + encryptor.finalize()
    
    # Encrypt the modified text
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    modified_ciphertext = encryptor.update(modified_text) + encryptor.finalize()

    # Compute differing bits
    bit_diff = xor_bytes(original_ciphertext, modified_ciphertext)
    total_bits = len(original_ciphertext) * 8
    avalanche_percentage = (bit_diff / total_bits) * 100

    return avalanche_percentage, original_ciphertext, modified_ciphertext

def read_file_binary(file_path):
    """Reads a file in binary mode."""
    with open(file_path, 'rb') as file:
        return file.read()

def write_binary_file(file_path, data):
    """Writes binary data to a file."""
    with open(file_path, 'wb') as file:
        file.write(data)

# Parameters
BLOCK_SIZE = 16  # AES block size (128 bits)
key = secrets.token_bytes(16)  # AES-128 key (128-bit)
iv = secrets.token_bytes(16)  # Initialization vector (IV)

# File input
file_path = input("Enter the path to the file: ")  # Change this to your file path
original_plaintext = read_file_binary(file_path)

# Ensure plaintext is a multiple of BLOCK_SIZE (AES requirement)
padding_length = BLOCK_SIZE - (len(original_plaintext) % BLOCK_SIZE)
original_plaintext += bytes([padding_length]) * padding_length

# Flipping a single bit in the plaintext
modified_plaintext = bytearray(original_plaintext)
modified_plaintext[0] ^= 0b00000001  # Flip the least significant bit of the first byte
modified_plaintext = bytes(modified_plaintext)

# Compute Avalanche Effect
avalanche_percentage, original_ciphertext, modified_ciphertext = compute_avalanche_effect(
    original_plaintext, modified_plaintext, key, iv
)

# Output results
# print(f"Original Ciphertext: {binascii.hexlify(original_ciphertext).decode()}")
# print(f"Modified Ciphertext: {binascii.hexlify(modified_ciphertext).decode()}")
print(f"Avalanche Effect: {avalanche_percentage:.2f}% bit difference")

# Optionally, write encrypted data to files
# write_binary_file("original_encrypted.bin", original_ciphertext)
# write_binary_file("modified_encrypted.bin", modified_ciphertext)
