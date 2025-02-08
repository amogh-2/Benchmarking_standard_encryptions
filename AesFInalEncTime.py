import os
import time
import statistics
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Pin process to cores 0 and 1
os.system("taskset -cp 0,1 {}".format(os.getpid()))

def encrypt_file(file_path, key_size_bits=128):
    # Ask for file format
    file_format = input("Enter the file format you want to use (e.g., txt, jpg, mp4): ")
    
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size / (1024*1024) :.2f} MB")
    
    #encryption_times = []
    
    # for _ in range(2):  # Run encryption 100 times
    #     # Start benchmarking from file opening
    start_time = time.perf_counter()
        
        # Read file data
    with open(file_path, "rb") as f:
        data = f.read()

        
    # Generate AES key and IV
    key = os.urandom(key_size_bits // 8)
    iv = os.urandom(16)  # 16 bytes for AES-CBC
        
    # Initialize AES-CBC cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
        
    # Ensure data is a multiple of block size (16 bytes for AES)
    padding_length = 16 - (len(data) % 16)
    data += bytes([padding_length] * padding_length)
        
    # Perform encryption
    ciphertext = encryptor.update(data) + encryptor.finalize()
        
    # Save encrypted file
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as f:
        f.write(iv + ciphertext)  # Store IV at the beginning for decryption
        
    # End benchmarking
    end_time = time.perf_counter()
        
    # Calculate encryption time for this iteration
    encryption_time = end_time - start_time
    # encryption_times.append(encryption_time)
    
    # Calculate mean encryption time
    # mean_encryption_time = sum(encryption_times) / len(encryption_times)
    
    # Calculate standard deviation of encryption time
    # std_dev_encryption_time = statistics.stdev(encryption_times)
    
    # Calculate throughput (MB/s) using mean encryption time
    throughput = (file_size / 1024 / 1024) / encryption_time if encryption_time > 0 else 0
    
    # Results
    print(f"Mean Encryption Time (100 iterations): {encryption_time:.6f} seconds")
    # print(f"Standard Deviation of Encryption Time: {std_dev_encryption_time:.6f} seconds")
    print(f"Throughput: {throughput:.2f} MB/s")
    print(f"Encrypted file saved as: {encrypted_file_path}")
    return encryption_time, throughput, encrypted_file_path, key, iv

# Example usage
file_path = input("Enter the file path: ")  # Ask user for file path
encrypt_file(file_path)
