#!/usr/bin/python3

import mysql.connector
import getpass

class LivestockManagementSystem:
    VALID_LIVESTOCK_TYPES = ['cows', 'sheep', 'goats', 'chickens', 'fish', 'rabbits', 'pigs', 'turkeys', 'snails', 'rams']

    def __init__(self):
        self.conn = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10722874",
            password="uVcdncbub8",
            database="sql10722874"
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                phone_number VARCHAR(15) PRIMARY KEY,
                password VARCHAR(255),
                full_name VARCHAR(255),
                address VARCHAR(255)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livestock (
                id INT AUTO_INCREMENT PRIMARY KEY,
                phone_number VARCHAR(15),
                livestock_type VARCHAR(50),
                quantity INT,
                FOREIGN KEY (phone_number) REFERENCES accounts(phone_number)
            )
        """)
        self.conn.commit()

    def print_header(self, title):
        print("\n" + "." * 50)
        print(f"{title.center(50)}")
        print("." * 50 + "\n")

    def print_menu(self, options):
        print("\n" + "." * 50)
        for option in options:
            print(option)
        print("." * 50 + "\n")

    def create_account(self):
        self.print_header("Create an Account")
        full_name = input("Full Name: ")
        phone_number = input("Phone Number: ")
        address = input("Address: ")
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")

        if password != confirm_password:
            print("\nPasswords do not match! Please try again.")
            return False

        self.cursor.execute("""
            INSERT INTO accounts (phone_number, password, full_name, address)
            VALUES (%s, %s, %s, %s)
        """, (phone_number, password, full_name, address))
        self.conn.commit()
        print("\nAccount created successfully!")
        return True

    def login(self):
        self.print_header("Login")
        phone_number = input("Phone Number: ")
        password = getpass.getpass("Password: ")

        self.cursor.execute("""
            SELECT * FROM accounts WHERE phone_number = %s AND password = %s
        """, (phone_number, password))
        account = self.cursor.fetchone()

        if account:
            print("\nLogin successful!")
            return phone_number
        else:
            print("\nInvalid phone number or password!")
            return None

    def display_livestock_options(self):
        print("Please select a type of livestock:")
        for index, livestock in enumerate(self.VALID_LIVESTOCK_TYPES, start=1):
            print(f"{index}. {livestock.capitalize()}")
        choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= choice <= len(self.VALID_LIVESTOCK_TYPES):
            return self.VALID_LIVESTOCK_TYPES[choice - 1]
        else:
            print("\nInvalid choice! Please try again.")
            return self.display_livestock_options()

    def add_livestock_data(self, phone_number):
        self.print_header("Adding Livestock Data")
        livestock_type = self.display_livestock_options()
        quantity = input("Quantity: ")

        self.cursor.execute("""
            INSERT INTO livestock (phone_number, livestock_type, quantity)
            VALUES (%s, %s, %s)
        """, (phone_number, livestock_type, quantity))
        self.conn.commit()
        print("\nLivestock data added successfully!")

    def update_livestock_data(self, phone_number):
        self.print_header("Updating Livestock Data")
        livestock_type = self.display_livestock_options()

        self.cursor.execute("""
            SELECT * FROM livestock WHERE phone_number = %s AND livestock_type = %s
        """, (phone_number, livestock_type))
        livestock = self.cursor.fetchone()

        if livestock:
            new_quantity = input("New Quantity: ")
            self.cursor.execute("""
                UPDATE livestock
                SET quantity = %s
                WHERE phone_number = %s AND livestock_type = %s
            """, (new_quantity, phone_number, livestock_type))
            self.conn.commit()
            print("\nLivestock data updated successfully!")
        else:
            print("\nLivestock type not found!")

    def view_livestock_data(self, phone_number):
        self.print_header("Viewing Livestock Data")
        self.cursor.execute("""
            SELECT livestock_type, quantity FROM livestock WHERE phone_number = %s
        """, (phone_number,))
        data_found = False
        for (livestock_type, quantity) in self.cursor:
            print(f"\nLivestock Type: {livestock_type.capitalize()}, Quantity: {quantity}")
            data_found = True
        if not data_found:
            print("\nNo livestock data found!")

    def check_loan_eligibility(self, phone_number):
        self.print_header("Checking Loan Eligibility")
        livestock_data = {}
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

        self.cursor.execute("""
            SELECT livestock_type, quantity FROM livestock WHERE phone_number = %s
        """, (phone_number,))
        for livestock_type, quantity in self.cursor:
            livestock_data[livestock_type] = int(quantity)

        eligible = False
        lacking = []
        for livestock, count in eligibility_conditions.items():
            if livestock_data.get(livestock, 0) >= count:
                eligible = True
            else:
                lacking.append((livestock, count - livestock_data.get(livestock, 0)))

        if eligible:
            print("\nYou are eligible for a loan!")
        else:
            print("\nYou are not eligible for a loan!")
            for livestock, shortfall in lacking:
                print(f"You need {shortfall} more {livestock} to be eligible for a loan.")

    def delete_account(self, phone_number):
        self.print_header("Deleting Account")
        confirmation = input("Are you sure you want to delete your account? (yes/no): ").lower()

        if confirmation != 'yes':
            print("\nAccount deletion cancelled.")
            return

        self.cursor.execute("""
            DELETE FROM accounts WHERE phone_number = %s
        """, (phone_number,))
        self.cursor.execute("""
            DELETE FROM livestock WHERE phone_number = %s
        """, (phone_number,))
        self.conn.commit()
        print("\nAccount deleted successfully!")

    def delete_livestock_data(self, phone_number):
        self.print_header("Deleting Livestock Data")
        livestock_type = self.display_livestock_options()

        self.cursor.execute("""
            DELETE FROM livestock WHERE phone_number = %s AND livestock_type = %s
        """, (phone_number, livestock_type))
        self.conn.commit()
        print("\nLivestock data deleted successfully!")

    def main_menu(self):
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
        while True:
            self.print_header("Main Menu")
            self.print_menu([
                "1. Adding livestock data",
                "2. Updating livestock data",
                "3. Viewing livestock data",
                "4. Checking loan eligibility",
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
