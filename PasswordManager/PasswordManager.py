# A program for managing passwords securely
# It allows users to store, retrieve, and manage their passwords with encryption
import os
import json
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, storage_file='passwords.json', key_file='secret.key'):
        """
        Initialize the PasswordManager with storage and encryption key files.
        Args:
            storage_file (str): File to store encrypted passwords.
            key_file (str): File to store the encryption key.
        """
        self.storage_file = storage_file
        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)
        self.passwords = self.load_passwords()

    def load_or_generate_key(self):
        """Load existing encryption key or generate a new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
            return key

    def load_passwords(self):
        """
        Load and decrypt passwords from the storage file.
        Returns:
            dict: Decrypted passwords dictionary or empty dict if file doesn't exist.
        """
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'rb') as file:
                    encrypted_data = file.read()
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    return json.loads(decrypted_data)
            return {}
        except Exception as e:
            print(f"Error loading passwords: {e}")
            return {}

    def save_passwords(self):
        """
        Encrypt and save passwords to the storage file.
        """
        try:
            encrypted_data = self.cipher.encrypt(json.dumps(self.passwords).encode())
            with open(self.storage_file, 'wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            print(f"Error saving passwords: {e}")

    def add_password(self, service, username, password):
        """
        Add a new password entry for a service.
        Args:
            service (str): Name of the service.
            username (str): Username for the service.
            password (str): Password for the service.
        Returns:
            bool: True if added successfully, False if service already exists.
        """
        if not service or not username or not password:
            print("Service, username, and password cannot be empty.")
            return False
        if service in self.passwords:
            print(f"Service '{service}' already exists.")
            return False
        self.passwords[service] = {'username': username, 'password': password}
        self.save_passwords()
        return True

    def get_password(self, service):
        """
        Retrieve password entry for a service.
        Args:
            service (str): Name of the service.
        Returns:
            dict or None: Password entry if found, None otherwise.
        """
        return self.passwords.get(service, None)

    def delete_password(self, service):
        """
        Delete a password entry for a service.
        Args:
            service (str): Name of the service.
        Returns:
            bool: True if deleted successfully, False if service not found.
        """
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
            return True
        return False

    def list_services(self):
        """
        List all stored service names.
        Returns:
            list: List of service names.
        """
        return list(self.passwords.keys())


if __name__ == "__main__":
    try:
        pm = PasswordManager()
        while True:
            print("\nPassword Manager")
            print("1. Add Password")
            print("2. Get Password")
            print("3. Delete Password")
            print("4. List Services")
            print("5. Exit")
            choice = input("Choose an option: ").strip()

            if choice == '1':
                service = input("Enter service name: ").strip()
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                if pm.add_password(service, username, password):
                    print(f"Password for {service} added successfully.")
            elif choice == '2':
                service = input("Enter service name: ").strip()
                if not service:
                    print("Service name cannot be empty.")
                    continue
                entry = pm.get_password(service)
                if entry:
                    print(f"Service: {service}, Username: {entry['username']}, Password: {entry['password']}")
                else:
                    print(f"No entry found for {service}.")
            elif choice == '3':
                service = input("Enter service name: ").strip()
                if not service:
                    print("Service name cannot be empty.")
                    continue
                if pm.delete_password(service):
                    print(f"Password for {service} deleted successfully.")
                else:
                    print(f"No entry found for {service}.")
            elif choice == '4':
                services = pm.list_services()
                if services:
                    print("Stored services:")
                    for svc in services:
                        print(f"- {svc}")
                else:
                    print("No services stored.")
            elif choice == '5':
                print("Exiting Password Manager.")
                break
            else:
                print("Invalid option. Please choose a number between 1 and 5.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")