#!/bin/env python3

import os
import sys
import hashlib
import base64
from getpass import getpass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Setting Directories
auth_file = 'auth.data'
accounts_file = 'accounts.data'


def password_generator(min_chars=25, max_chars=45):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    random.seed = (os.urandom(1024))
    password = "".join(random.choice(all_chars)
                       for _ in range(random.randint(min_chars, max_chars)))
    return password


def add_accounts(auth_file,accounts_file):
    if os.path.isfile(accounts_file) :

        name = input('Name: ')
        email = input('Email: ')
        while True:
            gen = input('Auto Passgen ? ')
            if "y" in gen:
                password = getpass('Pass: ')
                break
            elif "n" in gen:
                password = input('Pass: ')
                break
            elif "n" in gen and "y" in gen:
                print("Im Confused")
                continue
            else:
                continue
        data = '|  {name}  |  {email}  |  {Password}  |\n'

        with open(accounts_file, 'a+') as f:
            f.write(data)


def system(auth_file,accounts_file):
    print('''
 |=============|
 |     |||     |
 |    || ||    |
 |   ||   ||   |
 |  |||||||||  |
 | ||       || |
 |=============|

 [*] Use Show (or 1) To See All Accounts
 [*] Use Add (or 2) To Add Account
 [*] Use Delete (or 3) To Delete All
 [*] Use Exit...
    ''')

    exited = False

    while not exited:
        choice = input(' $ ').lower()
        if choice in ["1","show"]:
            try:
                with open(accounts_file) as f:
                    print(f.read())
            except FileNotFoundError:
                print("No Accounts Found...")
        elif choice in ["2","add"]:
            add_accounts(auth_file,accounts_file,key_file)
        elif choice in ["3","delete"]:
            print("\nDeleted...\n")
            os.remove(accounts_file)
            os.mknod(accounts_file)
        elif choice in ["4","exit"]:
            exited = True
        else:
            continue


def register(auth_file,accounts_file):
    try: # Looking For Password **Might Improve Later**
        with open(auth_file):
            pass
            yn = input(" Password Found (If you proceed the account will be deleted) y/N ").lower()
            if "y" in yn:
                os.remove(auth_file)
                os.remove(accounts_file)
                os.mknod(auth_file)
                os.mknod(accounts_file)
            elif "y" in yn and "n" in yn: #Making sure people don't use yesn't
                print(" Im Confused...")
            else:
                pass
    except FileNotFoundError:
        pass

    while True:
        given_password = getpass(" Password: ").encode() #Bytes
        repeat_password = getpass(" Repeat: ").encode() #Bytes
        #Making Sure Passwords Are The Same Before Hashing
        if given_password == repeat_password:
            #Hashing Main Password
            master = hashlib.sha3_512(given_password).hexdigest()
            with open(auth_file, 'w') as reg_file:
                reg_file.write(master)  # Storing Password in file
                print("\n Success\n")
                break
        else:
            print(" Passwords Don't Match...")
            continue


def login(auth_file,accounts_file):
    exited = False

    print('''
 1 Login
 2 Register
 3 Exit
    ''')
    while not exited:
        choice = input(" $ ").lower()
        if choice in ["1","login"]:
            password = getpass('\n [User] Password: ').encode()
            hashed_password = hashlib.sha3_512(password).hexdigest() #Hashing Password
            print(hashed_password)
            if os.path.isfile(auth_file): #Looking For Password File
                with open(auth_file, 'r') as auth: #Reading File
                    auth_data = auth.read()
                if hashed_password == auth_data:
                    print("Success")
                    system(auth_file,accounts_file,key_file) #Start System
                    break
                else:
                    print("Failed...")
            else:
                print("No Passwords Found")
                os.mknod(auth_file)
        elif choice in ["2","register"]:
            register(auth_file,accounts_file,key_file)
        elif choice in ["3","exit"]:
            exited = True
        else:
            continue


try:
    login(auth_file,accounts_file)
except KeyboardInterrupt:
    print("Exiting...")
