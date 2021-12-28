import hashlib
import logging
import os
import re
from File_handler_module import File_Handler
from Log_handler_module import Log_handler
from datetime import datetime

class Sign_up:
    """
       attribute:
        username
        password

        methods :
        username_validation
        check_password
        check_sign_up: call check password and user validation
        cascading and make directory if all things are valid
    """

    def __init__(self , username , password):
        self.username = username
        self.password = password

    def username_validation(self):
        """
        open file/chck if username is in that file, check pattern of user
        :return is_valid:
        """

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
            print("username must start with a alphabetical characters\n"
                  "it can continue with alphabetical characters or numbers and _ ."
                  "\n it must contain at least 8 character upto 30")
        return is_valid

    def check_password(self):
        """
        call check username then check password and hash it with salt
        :return:
        """
        hashed_password = ''
        message = 'sign_up_failed'
        if self.username_validation():
            salt_file = File_Handler("salt.csv")
            try:
                salt_dic = salt_file.read()
            except FileNotFoundError:
                # salt does not exist
                print("Can not register because of lack of internal data error!")
                Log_handler.log('File_NotFoundException','EXCEPTION')
                return
            salt = salt_dic[0]['salt']
            if self.password!='' and re.fullmatch('^[A-Za-z0-9_@+|$&*;]{7,29}$'
                    ,self.password):
                hashed_password =  hashlib.sha512((self.password + salt).encode()).\
                    hexdigest()
                message = 'sign_up_successful'
            elif self.password == '':
                print("you must enter a password.")
            else:
                print("Password can contain A-Z , a-z , 0-9 , _ , @ $ & * ; \n"
                      "And it must be at least 7 upto 29 characters")

        dic_result = {'hashed_password':hashed_password ,'message':message}
        return dic_result

    def check_sign_up(self):
        """
        call check_password and check username indirectly
        add valid usrname and passwpord which is signed up, in username_password file
        :return:
        """
        dic_result = self.check_password()
        message = dic_result['message']
        hashed_password = dic_result['hashed_password']
        if message == 'sign_up_successful':
            path = "username_password.csv"
            fl = File_Handler(path)
            try:
                fl.write({'username':self.username,
                          'password':hashed_password , 'failed_login_count':0})
            except Exception as ex:
                print("Sign up failed!")
                print(ex.with_traceback())
                Log_handler.log(f'{ex.__str__()}','EXCEPTION')
            os.mkdir(f'users/{self.username}')
            os.mkdir(f'users/{self.username}/Inbox')
            os.mkdir(f'users/{self.username}/Sentbox')
            os.mkdir(f'users/{self.username}/Draft')
            path = (f'users/{self.username}/Intbox/index_file.csv')
            try:
                with open(path,'w')as csvfile:
                    pass
            except Exception as ex:
                print(ex.with_traceback())
                Log_handler.log(f'{ex.__str__()}', 'EXCEPTION')
            path = (f'users/{self.username}/Sentbox/index_file.csv')
            try:
                with open(path, 'w') as csvfile:
                    pass
            except Exception as ex:
                print(ex.with_traceback())
                Log_handler.log(f'{ex.__str__()}', 'EXCEPTION')
            path = (f'users/{self.username}/Draft/index_file.csv')
            try:
                with open(path, 'w') as csvfile:
                    pass
            except Exception as ex:
                print(ex.with_traceback())
                Log_handler.log(f'{ex.__str__()}', 'EXCEPTION')
            print("You have been signed up successfully!")
        Log_handler.log(message,'INFO')
        print(message)  #inform user if signed up successfully or not
