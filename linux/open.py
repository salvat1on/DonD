from cryptography.fernet import Fernet
import os

def load_key(key_file):
    return open(key_file, "rb").read()

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as file:
        encrypted_data = file.read()

    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    original_file_path = encrypted_file_path[:-len(".encrypted")]  # Remove the ".encrypted" extension
    with open(original_file_path, "wb") as file:
        file.write(decrypted_data)

    os.remove(encrypted_file_path)  # Optionally, you can remove the encrypted file

def decrypt_directory(directory_path, key):
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith(".encrypted"):
                encrypted_file_path = os.path.join(foldername, filename)
                decrypt_file(encrypted_file_path, key)

if __name__ == "__main__":
    directory_to_decrypt = "/path/to/directory/"  # Update with the actual path of the encrypted directory
    key_file = "encryption_key.key"

    # Load the encryption key
    key = load_key(key_file)

    # Decrypt the directory
    decrypt_directory(directory_to_decrypt, key)
    print(f"Directory '{directory_to_decrypt}' decrypted successfully.")
