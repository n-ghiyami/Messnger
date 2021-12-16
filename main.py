import os

from sign_up import Sign_up
from Login_module import Login
import Message_Directory

user_input = input("Enter 1 to sign up and 2 to login ")
if user_input =='1':
    username = input("Enter username: ")
    password = input("Enter password: ")
    s = Sign_up(username,password)
elif user_input == '2':
    username = input("Enter username: ")
    password = input("Enter password: ")
    path = Login(username, password)
    if path != '':
        directory_contents = os.listdir(path)
        print(directory_contents)

else:
    print("invalid input")

"""
create new message
switch to inbox/ sentbx /draft
"""
