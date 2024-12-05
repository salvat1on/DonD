from cryptography.fernet import Fernet
import platform
import os

operating_system = platform.system()

target_drive = ""

if operating_system == "Linux":
    target_drive = "/path/to/directory/"
elif operating_system == "Windows":
    target_drive = "C:\\path\to\directory\"
else:
    print(f"Unknown operating system: {operating_system}")
        
def load_key(key_file):
    return open(key_file, "rb").read()

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as file:
        encrypted_data = file.read()

    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    original_file_path = encrypted_file_path[:-len(".encrypted")]
    with open(original_file_path, "wb") as file:
        file.write(decrypted_data)

    os.remove(encrypted_file_path)

def decrypt_directory(directory_path, key):
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith(".encrypted"):
                encrypted_file_path = os.path.join(foldername, filename)
                decrypt_file(encrypted_file_path, key)

if __name__ == "__main__":
    directory_to_decrypt = target_drive
    key_file = "encryption_key.key"

    key = load_key(key_file)

    decrypt_directory(directory_to_decrypt, key)
    print(f"Directory '{directory_to_decrypt}' decrypted successfully.")
