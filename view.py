#!/usr/bin/python3

import csv

ACCOUNTS_FILE = 'accounts.csv'

def view_accounts():
    """Prints out all accounts stored in the ACCOUNTS_FILE."""
    try:
        with open(ACCOUNTS_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("Accounts:")
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"{ACCOUNTS_FILE} not found!")

if __name__ == "__main__":
    view_accounts()
