import hashlib
from File_handler_module import File_Handler
from Log_handler import Log_handler
from datetime import datetime

class Login:

    def __init__(self , username , password):
        self.username = username
        self.password = password
        self.token='invalid'


    def does_username_exist(self):
        salt_file = File_Handler("salt.csv")
        salt_dic = salt_file.read()
        salt = salt_dic[0]['salt']
        #open file/chck if username is in that file, return dic['hashed_password']
        hashed_password = ''

        path = str(f"username_password.csv")
        fl = File_Handler(path)
        user_pass_list = fl.read()
        for item in user_pass_list:
            if self.username == item['username']:
                hashed_password = hashlib.sha512((self.password + salt).encode()).hexdigest()
                break
        return hashed_password

    def is_password_correct(self):
        event_type = 'login_failed'
        hashed_password = self.does_username_exist()
        print(hashed_password)
        if hashed_password!=''and hashed_password == self.hashed_password:
            self.token = 'valid'
            event_type = 'login_successfull'
        self.log = Log_handler.log_handler(self.username, datetime.now(), event_type)
        return self.token

a = Login('narges', '11a1')
print(a.is_password_correct())
