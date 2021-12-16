import hashlib
from File_handler_module import File_Handler
from Log_handler import Log_handler
from datetime import datetime

class Login:
    """
           attribute:
            username
            password
            token: for login session

            methods :
            username_validation
            check_password
            check_sign_up: call check password and user validation cascadingly and make directory if all things are valid
        """

    def __init__(self , username , password):
        self.username = username
        self.password = password
        self.token='invalid'


    def username_validation(self):

        #open file/chck if username is in that file, return dic['hashed_password']
        hashed_password = ''

        path = str(f"username_password.csv")
        fl = File_Handler(path)
        user_pass_list = fl.read()
        for item in user_pass_list:
            if self.username == item['username']:
                salt_file = File_Handler("salt.csv")
                salt_dic = salt_file.read()
                salt = salt_dic[0]['salt']
                hashed_password = hashlib.sha512((self.password + salt).encode()).hexdigest()
                break
        return hashed_password

    def check_password(self):
        event_type = 'login_failed'
        hashed_password = self.username_validation()
        print(hashed_password)
        if hashed_password!=''and hashed_password == self.hashed_password:
            self.token = 'valid'
            event_type = 'login_successfull'
        self.log = Log_handler.log_handler(self.username, datetime.now(), event_type)
        return self.token

    def login_method(self):
        path = ''
        self.token = self.check_password()
        if self.token == 'valid':
            path = f"{self.username}"
        return path