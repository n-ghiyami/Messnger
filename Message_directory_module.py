import os
from File_handler_module import File_Handler
import pandas as pd

class Homepage:
    """
    attribute:
    path : path of directory
    homepage_list : list of folders in homepage incuding inbox/sentbox/draft

    methods:
    load_homepage
    load_all_messages_from_directory : load messges from inbox/sentbox or draft
    create_new_message

    """

    def __init__(self, path):
        self.path = path

    def load_homepage(self):
        """
        this method loads homepage including inbox, sentbox and draft
        """
        if self.path != '':
            directory_contents = os.listdir(self.path)
            return (directory_contents)

    def load_all_messages_from_directory(self,directory_name):
        """
        This method loads all messages list from any given directory including inbox, sentbox or draft
        """
        all_messages = pd.read_csv(f"{os.getcwd()}/{directory_name}/index_file")
        print(f"total messages:{all_messages.index}\n",
              (f"{x+1} sender: {all_messages.loc[x,'sender']} "
              f"receiver {all_messages.loc[x,'receiver']} "
              f"unique_id: {all_messages.loc[x, 'unique_id']} "
              f"read status: {all_messages.loc[x, 'read_status']}" if directory_name == 'Inbox' else ''
              for x in all_messages.index))

    def create_new_message(self , input_text , receiver_address,sender_address):
        """
        this method creates a new message
        """
        new_message = Message.add_message(input_text,receiver_address,sender_address)
        return new_message

    def save_in_draft(self,temp_message):
        print("this method saves a specific message in draft")
        if self.path != '':
            path = f"{os.getcwd()}/Draft"
            fl = File_Handler(f"{path}/{temp_message.title}_{temp_message.time}.csv")
            fl.write(dict(temp_message))
            fl = File_Handler(f"{path}/index_file.csv")
            unique_id = f"{temp_message.title}_{temp_message.time}"
            content = fl.read()
            new_record = {'sender':temp_message.sender_address,'receiver':temp_message.receiver_address,
                          'unique_id':unique_id }
            content.append(new_record)
            fl.write(content)

    def show_message(self, path, message_number):
        """
        this method shows a specific message
        :param message_number:
        :return:
        """
        df = pd.read_csv(f"{path}/index_file")
        message_path = f"{path}/{df.loc[message_number-1 , 'unique_id']}.csv"
        message_df = pd.read_csv(message_path)
        message = Message.add_message(message_df.loc[0,'text'],
            message_df.loc[0,'receiver'],message_df.loc[0,'sender_address'],
            message_df.loc[0,'title'],message_df.loc[0,'time'])
        if path.endswith('Inbox'):
            df.loc[message_number-1 , 'read_status'] = 'read'
        df.to_csv(f"{path}/index_file")
        return str(message)

    def delete_message(self,path, message_number):
        """
        this method deletes a specific message from path folder
        :param path:
        :param message_number:
        :return:
        """
        df = pd.read_csv(f"{path}/index_file.csv")
        os.remove(f"{path}/{df.loc[message_number-1 , 'unique_id']}")
        df.drop(labels=message_number-1,axis=0)
        print("Message has just been deleted!")

    def send_message(self,temp_message):
        if self.path != '':
            path = f"{os.getcwd()}/Sentbox"
            unique_id = f"{temp_message.title}_{temp_message.time}"
            fl = File_Handler(f"{path}/{unique_id}.csv")
            fl.write(dict(temp_message))
            fl = File_Handler(f"{path}/index_file.csv")
            content = fl.read()
            new_record = {'sender':temp_message.sender_address,'receiver':temp_message.receiver_address,
                          'unique_id':unique_id }
            content.append(new_record)
            fl.write(content)
#           update receiver inbox
            os.chdir("..") #change directory to all users directory
            path = f"{os.getcwd()}/{temp_message.receiver_address}/Inbox"
            fl = File_Handler(f"{path}/{unique_id}_{temp_message.sender_address}.csv")
            # may some users send message simultaneously
            fl.write(dict(temp_message))
            fl = File_Handler(f"{path}/index_file.csv")
            content = fl.read()
            new_record = {'sender': temp_message.sender_address, 'receiver': temp_message.receiver_address,
                          'unique_id': unique_id, 'read_status':'unread'}
            content.append(new_record)
            fl.write(content)




class Message:
    """
    attributes:
    text
    receiver_address
    sender_address
    title
    time

    methods:
    check_address():checks whether receiver address exists
    """
    def __init__(self,text,receiver_address,sender_address , title , time):
        self.text = text
        self.receiver_address = receiver_address
        self.sender_address = sender_address
        self.title = title
        self.time = time

    @classmethod
    def add_message(cls,text,receiver_address,sender_address,title, time):
        if cls.check_address(receiver_address):
            new_message = cls(text , receiver_address , sender_address, title , time)
        else:
            new_message = None
        return new_message

    @classmethod
    def check_address(cls, username):
        is_valid =False
        fl = File_Handler("username_password.csv")
        content = fl.read()
        username_list = [item['username'] for item in content]
        if username in username_list:
            is_valid = True
        return is_valid

    def __str__(self):
        return f" sender: {self.sender_address} , receiver: {self.receiver_address}," \
               f" title: {self.title}, time: {self.time} \n{self.text}"

    def __dict__(self):
        return {'sender': f'{self.sender_address}' , 'receiver': f'{self.receiver_address}',\
               'title': f'{self.title}', 'time': f'{self.time}', 'text': f'{self.text}'}

class Recieved_message(Message):
    def __init__(self):
        super().__init__()
        self.read_status = 'unread'

    def make_reply_message(self):
        print("this method replys a specific message to sender")

    def make_forward_message(self, to_username):
        print("this method forwards a specific message")

class Sent_message(Message):
    def __init__(self):
        super().__init__()

    def make_forward_message(self, to_username):
        print("this method forwards a specific message")

class Draft_message(Message):
    def __init__(self):
        super().__init__()

    def switch_to_edit_mode(self, message_number):
        print("this method opens a specific message and let us edit it")

    def send_massage(self):
        print("this method send a specific message to a username and remove it from draft")


class Box:
    """
    attributes:
    message_list
    message_count

    methods:
    show_message
    delete_message
    """

    def __init__(self):
        super().__init__()
        self.message_list = []
        self.message_count = 0

    @staticmethod
    def show_message(self, path, message_number):
        """
        this method shows a specific message
        :param message_number:
        :return:
        """
        df = pd.read_csv(f"{path}/index_file")
        message_path = f"{path}/{df.loc[message_number-1 , 'unique_id']}.csv"
        message_df = pd.read_csv(message_path)
        message = Message.add_message(message_df.loc[0,'text'],
            message_df.loc[0,'receiver'],message_df.loc[0,'sender_address'],
            message_df.loc[0,'title'],message_df.loc[0,'time'])
        df.loc[message_number-1 , 'read_status'] = 'read'
        df.to_csv(f"{path}/index_file")
        return str(message)

    def delete_message(self,path, message_number):
        """
        this method deletes a specific message from path folder
        :param path:
        :param message_number:
        :return:
        """
        df = pd.read_csv(f"{path}/index_file.csv")
        os.remove(f"{path}/{df.loc[message_number-1 , 'unique_id']}")
        df.drop(labels=message_number-1,axis=0)
        print("Message has just been deleted!")
#
# class Inbox(Box):
#     def __init__(self):
#         super().__init__()
#
#
#
#     def reply_message(self):
#         print("this method replys a specific messageto sender")
#
#     def forward_message(self, to_username):
#         print("this method forwards a specific message")
#
#
# class Sentbox(Box):
#     def __init__(self):
#         super().__init__()
#
#     def forward_message(self, to_username):
#         print("this method forwards a specific message")

#
# class Draft(Box):
#     def __init__(self):
#         super().__init__()
#
#     def switch_to_edit_mode(self, message_number):
#         print("this method opens a specific message and let us edit it")
#
#     def send_message(self, to_username):
#         print("this method send a specific message to a username and remove it from draft")
#
#     def save_in_draft(self , path , temp_message):
#         """
#         :params:
#         :return:
#         """
#
#         fl = File_Handler(f"{os.getcwd()}/Draft/{temp_message.sender}")
#         fl.write(dict(temp_message))