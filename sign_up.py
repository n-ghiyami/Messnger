import hashlib

from File_handler_module import File_Handler
from Log_handler import Log_handler
from datetime import datetime

class Sign_up:



    def __init__(self , username , password):
        self.username = username
        self.password = password
        self.token='invalid'


    def username_validation(self):
        #open file/chck if username is in that file, return dic['hashed_password']

        is_valid = True
        path = str(f"username_password.csv")
        fl = File_Handler(path)
        user_pass_list = fl.read()
        for item in user_pass_list:
            if self.username == item['username']:
                print('Username exists!')
                break
        return

    def is_password_correct(self):
        hashed_password = ''
        event_type = 'sign_up_failed'
        if not self.username_validation():
            salt_file = File_Handler("salt.csv")
            salt_dic = salt_file.read()
            salt = salt_dic[0]['salt']
            if self.password!='':
                hashed_password =  hashlib.sha512((self.password + salt).encode()).hexdigest()
                event_type = 'sign_up_successful'
        self.log = Log_handler.log_handler(self.username, datetime.now(), event_type)
        return
