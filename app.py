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
        """Create a new user account using full name, phone number, address and password."""
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
    
    @staticmethod
    def login():
        """Log in an existing user using phone number and password."""
        LivestockManagementSystem.print_header("Login")
        phone_number = input("Phone Number: ")
        password = getpass.getpass("Password: ")

        with open(ACCOUNTS_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == phone_number and row[1] == password:
                    print("\nLogin successful!")
                    return phone_number
        print("\nInvalid phone number or password!")
        return None

    @staticmethod
    def display_livestock_options():
        """Display livestock options and get the user's choice."""
        print("Please select a type of livestock:")
        for index, livestock in enumerate(VALID_LIVESTOCK_TYPES, start=1):
            print(f"{index}. {livestock.capitalize()}")
        print(f"{len(VALID_LIVESTOCK_TYPES) + 1}. Cancel")
        choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= choice <= len(VALID_LIVESTOCK_TYPES):
            return VALID_LIVESTOCK_TYPES[choice - 1]
        elif choice == len(VALID_LIVESTOCK_TYPES) + 1:
            return None
        else:
            print("\nInvalid choice! Please try again.")
            return LivestockManagementSystem.display_livestock_options()
    
    def add_livestock_data(self, phone_number):
        """Add livestock data for a user."""
        self.print_header("Adding Livestock Data")
        livestock_type = self.display_livestock_options()
        if livestock_type is None:
            print("\nAction cancelled. Returning to main menu.")
            return

        quantity = input("Quantity: ")

        with open(LIVESTOCK_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([phone_number, livestock_type, quantity])
            print("\nLivestock data added successfully!")

    
    def update_livestock_data(self, phone_number):
        """Update livestock data for a user."""
        self.print_header("Updating Livestock Data")
        livestock_type = self.display_livestock_options()
        if livestock_type is None:
            print("\nAction cancelled. Returning to main menu.")
            return

        updated_rows = []
        found = False

        with open(LIVESTOCK_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == phone_number and row[1] == livestock_type:
                    new_quantity = input("New Quantity: ")
                    updated_rows.append([phone_number, livestock_type, new_quantity])
                    found = True
                else:
                    updated_rows.append(row)

        if not found:
            print("\nLivestock type not found!")
            return

        with open(LIVESTOCK_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
            print("\nLivestock data updated successfully!")

    def view_livestock_data(self, phone_number):
        """View livestock data for a user."""
        self.print_header("Viewing Livestock Data")
        with open(LIVESTOCK_FILE, mode='r') as file:
            reader = csv.reader(file)
            data_found = False
            for row in reader:
                if row[0] == phone_number:
                    print(f"\nLivestock Type: {row[1].capitalize()}, Quantity: {row[2]}")
                    data_found = True
            if not data_found:
                print("\nNo livestock data found!")

    def check_loan_eligibility(self, phone_number):
        """Check loan eligibility for a user based on livestock data."""
        self.print_header("Checking Loan Eligibility")
        livestock_data = {}

        with open(LIVESTOCK_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == phone_number:
                    livestock_data[row[1]] = int(row[2])

        # Loan eligibility criteria
        eligibility_conditions = {
            'cows': 10,
            'chickens': 100,
            'goats': 50,
            'fish': 500,
            'rabbits': 80,
            'pigs': 50,
            'turkeys': 100,
            'snails': 500,
            'rams': 20
        }

        eligible = any(livestock_data.get(livestock, 0) >= count for livestock, count in eligibility_conditions.items())

        if eligible:
            print("\nCongratulations!!! You are eligible for a loan!\nGo to any BK branch near you to apply for one.")
        else:
            print("\nYou are not eligible for a loan.")
            print("\nHere's what you need to be eligible for a loan:")
            for livestock, count in eligibility_conditions.items():
                current_count = livestock_data.get(livestock, 0)
                if current_count < count:
                    print(f" - {livestock.capitalize()}: You have {current_count}, but you need at least {count}.")

    def delete_account(self, phone_number):
        """Delete a user's account."""
        self.print_header("Deleting Account")
        confirmation = input("Are you sure you want to delete your account? (yes/no): ").lower()

        if confirmation != 'yes':
            print("\nAccount deletion cancelled.")
            return

        updated_rows = []

        with open(ACCOUNTS_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != phone_number:
                    updated_rows.append(row)

        with open(ACCOUNTS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
            print("\nAccount deleted successfully!")

    def delete_livestock_data(self, phone_number):
        """Delete livestock data for a user."""
        self.print_header("Deleting Livestock Data")
        livestock_type = self.display_livestock_options()
        if livestock_type is None:
            print("\nAction cancelled. Returning to main menu.")
            return

        updated_rows = []
        found = False

        with open(LIVESTOCK_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == phone_number and row[1] == livestock_type:
                    found = True
                else:
                    updated_rows.append(row)

        if not found:
            print("\nLivestock type not found!")
            return

        with open(LIVESTOCK_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
            print("\nLivestock data deleted successfully!")

    
    def main_menu(self):
        """Display the main menu and handle user choices."""
        while True:
            self.print_header("Welcome to the Livestock Management System")
            self.print_menu([
                "1. Create an account",
                "2. Login",
                "3. Exit"
            ])
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
                phone_number = self.login()
                if phone_number:
                    self.user_menu(phone_number)
            elif choice == '3':
                break
            else:
                print("\nInvalid choice! Please try again.")

    def user_menu(self, phone_number):
        """Display the user menu and handle user choices."""
        while True:
            self.print_header("Main Menu")
            self.print_menu([
                "1. Add livestock data",
                "2. Update livestock data",
                "3. View livestock data",
                "4. Check loan eligibility",
                "5. Delete livestock data",
                "6. Delete account",
                "7. Exit"
            ])
            menu_choice = input("Enter your choice: ")

            if menu_choice == '1':
                self.add_livestock_data(phone_number)
            elif menu_choice == '2':
                self.update_livestock_data(phone_number)
            elif menu_choice == '3':
                self.view_livestock_data(phone_number)
            elif menu_choice == '4':
                self.check_loan_eligibility(phone_number)
            elif menu_choice == '5':
                self.delete_livestock_data(phone_number)
            elif menu_choice == '6':
                self.delete_account(phone_number)
                break
            elif menu_choice == '7':
                break
            else:
                print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    system = LivestockManagementSystem()
    system.main_menu()           
