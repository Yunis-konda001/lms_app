#!/usr/bin/python3

import csv
import os
import getpass

ACCOUNTS_FILE = 'accounts.csv'
LIVESTOCK_FILE = 'livestock.csv'
VALID_LIVESTOCK_TYPES = ['cows', 'sheep', 'goats', 'chickens', 'fish', 'rabbits', 'pigs', 'turkeys', 'snails', 'rams']

class LivestockManagementSystem:
    """
    A class to manage livestock data and user accounts.
    """

    def __init__(self):
        self.ensure_files_exist()

    def ensure_files_exist(self):
        """Ensure the accounts and livestock files exist."""
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Phone Number', 'Password', 'Full Name', 'Address'])

        if not os.path.exists(LIVESTOCK_FILE):
            with open(LIVESTOCK_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Phone Number', 'Livestock Type', 'Quantity'])

    @staticmethod
    def print_header(title):
        """Print a formatted header."""
        print("\n" + "."*50)
        print(f"{title.center(50)}")
        print("."*50 + "\n")

    @staticmethod
    def print_menu(options):
        """Print a formatted menu."""
        print("\n" + "."*50)
        for option in options:
            print(option)
        print("."*50 + "\n")
    
    @staticmethod
    def create_account():
        """Create a new user account."""
        LivestockManagementSystem.print_header("Create an Account")
        full_name = input("Full Name: ")
        phone_number = input("Phone Number: ")
        address = input("Address: ")
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")

        if password != confirm_password:
            print("\nPasswords do not match! Please try again.")
            return False

        with open(ACCOUNTS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([phone_number, password, full_name, address])
            print("\nAccount created successfully!")
            return True

