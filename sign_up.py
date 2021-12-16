import hashlib
import os
import re


from File_handler_module import File_Handler
from Log_handler import Log_handler
from datetime import datetime

class Sign_up:
    """
       attribute:
        username
        password

        methods :
        username_validation
        check_password
        check_sign_up: call check password and user validation cascadingly and make directory if all things are valid
    """

    def __init__(self , username , password):
        self.username = username
        self.password = password



    def username_validation(self):
        #open file/chck if username is in that file, return dic['hashed_password']

        is_valid = True
        path = str(f"username_password.csv")
        fl = File_Handler(path)
        if re.fullmatch('^[A-Za-z][A-Za-z0-9_]{7,29}$',self.username):
            user_pass_list = fl.read()
            for item in user_pass_list:
                if self.username == item['username']:
                    print('Username exists!')
                    is_valid = False
                    break
        else:
            is_valid = False
        return is_valid

    def check_password(self):
        hashed_password = ''
        event_type = 'sign_up_failed'
        if self.username_validation():
            salt_file = File_Handler("salt.csv")
            salt_dic = salt_file.read()
            salt = salt_dic[0]['salt']
            if self.password!='':
                hashed_password =  hashlib.sha512((self.password + salt).encode()).hexdigest()
                event_type = 'sign_up_successful'
                print(hashed_password)
        return hashed_password , event_type

    def check_sign_up(self):
        hashed_password , event_type =self.check_password()
        if event_type == 'sign_up_successful':
            path = "username_password.csv"
            fl = File_Handler(path)
            fl.write({'username':self.username,'password':hashed_password})
            os.mkdir(f'{self.username}')
            os.mkdir(f'{self.username}/Intbox')
            os.mkdir(f'{self.username}/Sentbox')
            os.mkdir(f'{self.username}/Draft')
        self.log = Log_handler.log_handler(self.username, datetime.now(), event_type)
