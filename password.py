#! /bin/env python3

import os
import sys
import base64
import random
import pickle
import hashlib
from getpass import *
from cryptography.fernet import Fernet

password = []
size = 0

def password_generator(size):
    chars = []
    LETTERS = "!@#$%^&*()1234567890qwrtyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()"
    for i in range(size):
        chars.append(random.choice(LETTERS))
    password = "".join(chars)
    return password

def account_add():
    try:
        os.mknod('acc/accounts.data')
    except FileExistsError:
        pass
    except FileNotFoundError:
        os.mkdir('acc/')

    name = input('name: ')
    email = input('email: ')
    yesNo = input("Automatic Password Generation? ")
    yesNo=yesNo.lower()
    if "y" in yesNo:
        letter_size = input("How many letters? ")
        letter_size = int(letter_size)
        try:
            if letter_size >= 10:
                print("Alright")
                passw = password_generator(letter_size)
            else:
                print("Number Has To Be Over 10")
        except TypeError:
            print("Please Use A number")
    elif "n" in yesNo:
        print("Alright!")
        passw = getpass('pass: ')
    print(f'''
 So Is This Correct
 name: {name}
 email: {email}
 pass: {passw}
    ''')

    while True:
        yes = input("y/N ")
        yes = yes.lower()
        if not yes or "n" in yes:
            print("Alright Exiting")
            break
        elif "y" in yes:
            with open('acc/accounts.data','rb') as f:
                lines = f.read()
            combo = f'{name} | {email} | {passw}\n'
            with open('acc/accounts.data', 'a') as f:
                f.write(combo)
            print("Added Files")
            break
        else:
            pass
            continue


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
 4)Clear Lines
 5)Exit
        ''')
        choices = input(" > ")
        if choices == "1":
            try:
                with open('acc/accounts.data','rb') as f:
                    print("\n name   |  email  |  password")
                    print("-------------------------------")
                    for line in f:
                        print(line.decode())
            except FileNotFoundError:
                print("\nNo Accounts Found\n")
                os.mknod('acc/accounts.data')
        elif choices == "2":
            account_add()

        elif choices == "3":
            sure = input("\n Are You Sure You Want To Delete? ")
            if "y" in sure:
                os.remove('acc/accounts.data')
                print("Successfully Deleted...")
            else:
                continue
        elif choices == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choices == "5":
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
    print("Exiting...")
    sys.exit()
