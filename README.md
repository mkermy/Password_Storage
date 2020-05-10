# Account Storage

This system is used to store account details(emails,passwords...) locally on your machine

## How It Works  

#### [Auth.data](https://github.com/mkermy/Password_Storage/blob/master/auth/auth.data)
Firstly, the auth.data file is used to store the main master password that is used to use the program
The password (The Default Password is 1, this can be changed by registering) which is chosen by user is written to the file then checked everytime the user logs in...

#### [Key.key](https://github.com/mkermy/Password_Storage/blob/master/auth/key.key)
You Might See a key.key File Which is used to store encryption keys (however this is **not** hard coded the encryption key changes when you password (stored in Auth.data) changes)
Everytime the user trys to read their data it goes back to this file decrypt the data.

#### [Accounts.data](https://github.com/mkermy/Password_Storage/blob/master/accounts/accounts.data)
This File holds all the user data but this data is encrypted and decrypted using the Key.key file.

## License 
This Project is covered under the [MIT license](https://github.com/mkermy/Password_Storage/blob/master/LICENSE).
