import os
from File_handler import File_Handler
class Message_directory:
    def __init__(self , path):
        self.path = path
        self.homepage_list = []

    def load_homepage(self):
        # self.homepage_list = os.listdir(self.path)
        print("this method loads homepage incuding inbox, sentbox and draft")

    def load_all_messages_from_directory(self):
        print("this method loads all messages list from any given directory including inbox, sentbox or draft")

    def create_new_message(self):
        print("this method creates a new message")

    def logout(self):
        print("this method logs out current user")

class Box:

    def __init__(self):
        super().__init__()
        self.message_list = []
        self.message_count = 0

    def show_message(self, message_number):
        print("this method shows a specific message")

    def delete_message(self, message_number):
        print("this method deletes a specific message")

class Inbox(Box):
    def __init__(self):
        super().__init__()

    def save_in_draft(self,):
        print("this method saves a specific message in draft")

    def reply_message(self):
        print("this method replys a specific messageto sender")

    def forward_message(self, to_username):
        print("this method forwards a specific message")

class Sentbox(Box):
    def __init__(self):
        super().__init__()

    def forward_message(self, to_username):
        print("this method forwards a specific message")


class Draft(Box):
    def __init__(self):
        super().__init__()

    def switch_to_edit_mode(self,message_number):
       print("this method opens a specific message and let us edit it")

    def send_message(self, to_username):
        print("this method send a specific message to a username and remove it from draft")

