import psutil
import platform
import os
# Get system information
os_name = platform.system()
processor = platform.processor()
cpu_count = psutil.cpu_count()
# Print results
    
print(f"OS: {os_name}")
print(f"Processor: {processor}")

