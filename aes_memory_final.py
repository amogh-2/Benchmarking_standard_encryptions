import os
import psutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import time

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Memory in MB

def aes_encrypt(file_data, key):
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create a cipher object with AES algorithm and CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply padding to the plain text
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()
    print(f"Memory after padding: {get_memory_usage():.2f} MB")

    # Encrypt the padded text
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv, cipher_text

# def aes_decrypt(cipher_text, key, iv):
#     # Create a cipher object with AES algorithm and CBC mode
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()

#     # Decrypt the cipher text
#     decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()

#     # Remove padding
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     unpadded_text = unpadder.update(decrypted_data) + unpadder.finalize()
#     return unpadded_text

def read_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: File not found!")
        return None
    except OSError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Generate a random 16-byte key for AES
    key = os.urandom(16)

    # Get file input from user
    file_path = input("Enter the full path to the file (e.g., C:\\Users\\acer\\Downloads\\10MBrandomfile.txt): ").strip()

    # Read file
    file_data = read_file(file_path)

    if file_data:
        file_size = len(file_data)  # Get size in bytes
        print(f"\nTesting with file of size {file_size / 1024:.2f} KB")

        # Measure memory usage before encryption
        memory_before_encryption = get_memory_usage()
        print(f"Memory before encryption: {memory_before_encryption:.2f} MB")

        # Encrypt the data
        iv, cipher_text = aes_encrypt(file_data, key)
        memory_after_encryption = get_memory_usage()
        print(f"Memory after encryption: {memory_after_encryption:.2f} MB")

        # Decrypt the data
        # decrypted_data = aes_decrypt(cipher_text, key, iv)
        # memory_after_decryption = get_memory_usage()
        # print(f"Memory after decryption: {memory_after_decryption:.2f} MB")
        print(f"actual memory usage:{memory_after_encryption-memory_before_encryption}")
        print(f"actual AES memory usage:{(memory_after_encryption-memory_before_encryption)-file_size/(1024*1024)}")
        

        # Optionally, save the decrypted data to a file if needed
        # output_file = "decrypted_" + os.path.basename(file_path)
        # with open(output_file, "wb") as f:
        #     f.write(decrypted_data)
        # print(f"Decrypted file saved as {output_file}")
