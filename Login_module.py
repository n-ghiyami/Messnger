import hashlib
from File_handler_module import File_Handler
from Log_handler_module import Log_handler
from datetime import datetime
from Message_directory_module import Homepage
class Login:
    """
           attribute:
            username
            password
            token: for login session

            methods :
            username_validation
            check_password
            check_sign_in: call check password and user validation cascadingly and make directory if all things are valid
        """

    def __init__(self , username , password):
        self.username = username
        self.password = password
        self.token='invalid'


    def username_validation(self):

        #open file/chck if username is in that file, return dic['hashed_password']
        hashed_password = ''
        password = ''
        path = f"username_password.csv"
        fl = File_Handler(path)
        user_pass_list = fl.read()
        for item in user_pass_list:
            if self.username == item['username']:
                password = item['password']
                break
        return password

    def check_password(self):
        # message = 'login_failed'
        stored_password = self.username_validation()
        if stored_password != '':
            salt_file = File_Handler("salt.csv")
            salt_dic = salt_file.read()
            salt = salt_dic[0]['salt']
            hashed_password = hashlib.sha512((self.password + salt).encode()).hexdigest()
            if hashed_password == stored_password:
                self.token = 'valid'
                # message = 'login_successfull'
        # self.log = Log_handler.log_handler(self.username, datetime.now(), event_type)
        return self.token

    def login_method(self):
        l = Log_handler()
        self.check_password()
        if self.token == 'valid':
            l.log(datetime.utcnow,'login_successfull', 'INFO')
            path = f"{self.username}"
            homepage = Homepage(path)
            homepage.load_homepage()
        else:
            print("Incorrect username or password!")
            l.log(datetime.utcnow,'login_failed','INFO')
        return self.token