#!/usr/bin/python3

import csv
import os
import getpass

ACCOUNTS_FILE = 'accounts.csv'
LIVESTOCK_FILE = 'livestock.csv'
VALID_LIVESTOCK_TYPES = ['cows', 'sheep', 'goats', 'chickens', 'fish', 'rabbits', 'pigs', 'turkeys', 'snails', 'rams']
