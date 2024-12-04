from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def load_key(key_file):
    return open(key_file, "rb").read()

def save_key(key, key_file):
    with open(key_file, "wb") as key_file:
        key_file.write(key)

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)

    encrypted_file_path = file_path + ".encrypted"  # Add a different tag to the encrypted file
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)

    os.remove(file_path)  # Optionally, you can remove the original unencrypted file

def encrypt_directory(directory_path, key):
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            encrypt_file(file_path, key)

if __name__ == "__main__":
    directory_to_encrypt = "/path/to/directory/"
    key_file = "encryption_key.key"

    # Generate or load the encryption key
    if not os.path.exists(key_file):
        key = generate_key()
        save_key(key, key_file)
    else:
        key = load_key(key_file)

    # Encrypt the directory
    encrypt_directory(directory_to_encrypt, key)
    print(f"Directory '{directory_to_encrypt}' encrypted successfully.")
