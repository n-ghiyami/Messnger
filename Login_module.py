import hashlib
from File_handler_module import File_Handler
from Log_handler_module import Log_handler
from datetime import datetime
from Message_directory_module import Messenger
import pandas as pd

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
                if int(item['failed_login_count']) >= 3:
                    print('Your account is locked! ')
                else:
                    password = item['password']
                break
        return password

    def check_password(self):
        stored_password = self.username_validation()
        if stored_password != '':
            try:
                salt_file = File_Handler("salt.csv")
            except FileNotFoundError:
                # salt does not exist
                print("Can not register because of lack of internal data error!")
                Log_handler.log('File_NotFoundException','EXCEPTION')
                return
            try:
                salt_dic = salt_file.read()
            except Exception as ex:
                print(f"{ex.__str__()}")
                Log_handler.log('File_NotFoundException','EXCEPTION')
                return
            salt = salt_dic[0]['salt']
            hashed_password = hashlib.sha512((self.password + salt).encode()).hexdigest()
            if hashed_password == stored_password:
                self.token = 'valid'
        return self.token

    def login_method(self):
        self.check_password()
        message = 'login_failed'
        if self.token == 'valid':
            path = f"{self.username}"
            message = 'login_successful'
            try:
                df = pd.read_csv(f"username_password.csv")
                for x in df.index:
                    if df.loc[x, 'username'] == self.username:
                        df.loc[x, 'failed_login_count'] = 0
                        df.to_csv("username_password.csv", index=None, index_label=None)
                        break
            except Exception as ex:
                print(f"{ex.__str__()}")
                Log_handler.log('File_exception','EXCEPTION')

        else:
            print("Incorrect username or password!")
            try:
                df = pd.read_csv('username_password.csv')
                if len(df) > 0:
                    for x in df.index:
                        if df.loc[x, "username"] == self.username:
                            df.loc[x, "failed_login_count"] = int(df.loc[x, "failed_login_count"]) + 1
                            df.to_csv('username_password.csv')
                            if df.loc[x, "failed_login_count"] == 3:
                                Log_handler.log(datetime.utcnow(), f'{self.username} account_locked', 'INFO')
                                print('Your account has been locked')
                            break
            except Exception as ex:
                print(f"{ex.__str__()}")
                Log_handler.log('File_exception','EXCEPTION')
                return
        Log_handler.log(datetime.utcnow,message,'INFO')
        return self.token