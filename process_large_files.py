import sys
import os
import subprocess

def compress_folder(folder_path, max_size=50):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
            if file_size > max_size:
                zip_file_path = file_path + '.zip'
                subprocess.run(['zip', '-j', zip_file_path, file_path])
                os.remove(file_path)
                print(f"Compressed {file_path} to {zip_file_path}")

def decompress_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                subprocess.run(['unzip', '-o', zip_file_path, '-d', root])
                os.remove(zip_file_path)
                print(f"Decompressed {zip_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_large_files.py compress|decompress")
        sys.exit(1)
    
    function_name = sys.argv[1]
    
    if function_name == "compress":
        compress_folder('./data', max_size=50)
    elif function_name == "decompress":
        decompress_folder('./data')
    else:
        print(f"Function {function_name} not found.")   
