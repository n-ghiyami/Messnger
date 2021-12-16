import os

from sign_up import Sign_up
from Login_module import Login
import Message_directory_module

user_input = input("Enter 1 to sign up and 2 to login ")
if user_input =='1':
    username = input("Enter username: ")
    password = input("Enter password: ")
    s = Sign_up(username,password)
elif user_input == '2':
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_obj = Login(username, password)
    login_obj.login_method()
else:
    print("invalid input")

"""
create new message
switch to inbox/ sentbox /draft
"""
