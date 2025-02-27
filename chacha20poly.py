import numpy as np
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def read_file_bytes(file_path):
    """Reads file as bytes."""
    with open(file_path, "rb") as f:
        return f.read()

def write_file_bytes(file_path, data):
    """Writes bytes to a file."""
    with open(file_path, "wb") as f:
        f.write(data)

def pad_data(data):
    """Pads data to be a multiple of 64 bytes (ChaCha20 block size)."""
    pad_len = 64 - (len(data) % 64)
    return data + bytes([0] * pad_len)

def encrypt_chacha20_poly1305(key, nonce, plaintext):
    """Encrypts data using ChaCha20-Poly1305."""
    cipher = ChaCha20Poly1305(key)
    return cipher.encrypt(nonce, plaintext, None)  # No additional data (AAD)

def decrypt_chacha20_poly1305(key, nonce, ciphertext):
    """Decrypts data using ChaCha20-Poly1305."""
    cipher = ChaCha20Poly1305(key)
    return cipher.decrypt(nonce, ciphertext, None)  # No additional data (AAD)

def correlation_coefficient(data1, data2):
    """Computes correlation coefficient between two byte sequences."""
    arr1 = np.frombuffer(data1, dtype=np.uint8)
    arr2 = np.frombuffer(data2, dtype=np.uint8)

    min_len = min(len(arr1), len(arr2))
    arr1, arr2 = arr1[:min_len], arr2[:min_len]  # Trim to same size

    return np.corrcoef(arr1, arr2)[0, 1]

def main():
    file_path = input("Enter the path of the file: ").strip()

    if not os.path.exists(file_path):
        print("File not found!")
        return

    # Generate random key (256-bit) and nonce (12-byte)
    key = os.urandom(32)  # 32 bytes = 256 bits
    nonce = os.urandom(12)  # ChaCha20-Poly1305 nonce is 12 bytes

    original_data = read_file_bytes(file_path)
    padded_data = pad_data(original_data)  # Padding ensures consistent comparison

    # Encrypt and Decrypt
    encrypted_data = encrypt_chacha20_poly1305(key, nonce, padded_data)
    decrypted_data = decrypt_chacha20_poly1305(key, nonce, encrypted_data)

    # Compute correlation coefficients
    corr_orig_cipher = correlation_coefficient(padded_data, encrypted_data)
    corr_orig_decrypted = correlation_coefficient(padded_data, decrypted_data)

    print(f"\nCorrelation Coefficient (Original vs Ciphertext): {corr_orig_cipher:.6f}")
    print(f"Correlation Coefficient (Original vs Decrypted): {corr_orig_decrypted:.6f}")

    # Save encrypted and decrypted files (optional)
    write_file_bytes("encrypted_file.bin", encrypted_data)
    write_file_bytes("decrypted_file.bin", decrypted_data)

    print("\nEncrypted and decrypted files saved.")

if __name__ == "__main__":
    main()
