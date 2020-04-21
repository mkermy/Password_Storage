#! /bin/env python3

import os
import sys
import base64
import pickle
import hashlib
import sqlite3
from getpass import *
from cryptography.fernet import Fernet

password = []



def system():
    try:
        os.mkdir('acc/')
    except FileExistsError:
        pass
    while True:
        print('''
 1)Show All Accounts
 2)Add An Account
 3)Delete All Account
 4)Exit
        ''')
        choices = input(" > ")
        if choices == "1":
            pass
        elif choices == "2":
            pass
        elif choices == "3":
            sure = input("\n Are You Sure You Want To Delete? ")
            if "y" in sure:
                pass
                print("Successfully Deleted...")
            else:
                continue
        elif choices == "4":
            sys.exit()
        else:
            continue


def register(password_list):
    try:
        with open("auth.data", 'rb') as f:
            yn = input("Are You Sure Account Already Found (If You Type Yes The Account Will BE DELETED) ")
            os.remove("auth.data")
    except FileNotFoundError:
        yn = input("Do You Want To Register? ")
    while True:
        if "y" in yn:
            master_password = getpass("Password: ").encode()
            repeat_password = getpass("Repeat Pass: ").encode()

            if len(master_password.decode()) >= 8:
                hashed_master = hashlib.sha3_512(master_password).hexdigest()
                hashed_repeat = hashlib.sha3_512(repeat_password).hexdigest()
                if hashed_master == hashed_repeat:
                    os.mknod("auth.data")
                    password_list.append(hashed_master)
                    with open("auth.data", 'wb') as f:
                        pickle.dump(password_list, f)
                    print("Successfully registered...")
                    login(password_list)
                    break
                else:
                    print("\nPassword Do Not Match")
            else:
                print("Password Too Short (8 letters or more)...")
        if "n" in yn:
            print("Alright...")
            login(password_list)
            break
        else:
            continue

def login(password_list):
    while True:
        print('''
 1)Login
 2)Register
 3)Exit
     ''')
        use = input(" > ")
        if use == "1":
            try:
                with open("auth.data", 'rb') as f:
                    auth = pickle.load(f)
                    print("\nLogin:")
                    password = getpass("\nPassword: ").encode()
                    hash_pass = hashlib.sha3_512(password).hexdigest()
                    if hash_pass in auth:
                        print("\nLogged in...")
                        system()
                    else:
                        print("Incorrect...")
                        continue
            except FileNotFoundError:
                print("No Passwords Found")
        elif use == "2":
            print("\nRegister")
            register(password_list)
            break
        elif use == "3":
            sys.exit()
        else:
            continue


try:
    login(password)
except KeyboardInterrupt:
    print("\nKeyboard Interrupt")
    sys.exit()
