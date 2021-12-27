import datetime
import os
from sign_up import Sign_up
from Login_module import Login
import Message_directory_module
from File_handler_module import File_Handler

while True:
    user_input = input("Enter 1 to sign up and 2 to login or any other key to exit : ")
    if user_input == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        s = Sign_up(username, password)
        s.check_sign_up()
    elif user_input == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_obj = Login(username, password)
        login_obj.login_method()
        if login_obj.token == 'valid':
            print("You're logged in!")
            while True:
                requested_function = input("Enter 1 to switch to folders or 2 to create "
                                           "a new message and 3 to logout: ")
                messenger_obj = Message_directory_module.Messenger(f"{username}")
                directory_list = messenger_obj.load_homepage()
                if requested_function == '1':
                    list_string = [f"{i} to {item}" for i, item in enumerate(directory_list, start=1)]
                    directory_number = int(input(f"Enter {','.join(list_string)}"))
                    directory_name = directory_list[directory_number - 1]
                    try:
                        if os.stat('index_file.csv').st_size == 0:
                            print("Folder is Empty")
                        else:
                            print(messenger_obj.load_all_messages_from_directory(directory_name))
                    except OSError:
                        print("No File to read!")
                    while True:
                        requested_function = input("Enter 1 to delete message and 2 to show message"
                                                   " and 3 to quit folder: ")
                        if requested_function == '1':
                            messenger_obj.load_all_messages_from_directory(directory_name)
                            message_number = int(input("Enter message number showed in left side of"
                                                       " record to delete: "))
                            messenger_obj.delete_message(directory_name,message_number)
                        elif requested_function == '2':
                            message_number = int(input("Enter message number showed in left side of"
                                                       " record to show: "))
                            print(messenger_obj.show_message(directory_name, message_number))
                        elif requested_function =='3':
                            break
                        else:
                            print("Invalid Input")

                elif requested_function == '2':
                    receiver_address = input("Enter receiver address: ")
                    title = input("Enter title of message: ")
                    text = input("Enter text of message: ")
                    time =  f"{datetime.datetime.utcnow().strftime( '%Y-%B-%d_%H-%M-%S')}"
                    new_message = messenger_obj.create_new_message(input_text=text,
                                                                   receiver_address=receiver_address,
                                                                   sender_address=username,
                                                                   title= title,time= time)
                    while True:
                        requested_function = input("Enter 1 to save in draft and 2 to send and 3 to discard: ")
                        if requested_function == '1':
                            messenger_obj.save_in_draft(new_message)
                            break
                        elif requested_function == '2':
                            messenger_obj.send_message(new_message)
                            break
                        elif requested_function == '3':
                            break
                        else:
                            print("invalid input")
                elif requested_function == 3:
                    print("your logged out")
                    break
                else:
                    print("invalid input")
    else:
        break
