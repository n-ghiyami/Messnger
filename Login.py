import hashlib ,uuid
import File_handler
from Log_handler import Log_handler
from datetime import datetime

class Login:

    salt = uuid.uuid4().hex

    def __init__(self , username , password):
        self.username = username
        self.hashed_password = hashlib.sha512((password + Login.salt).encode()).hexdigest()
        self.token='invalid'


    def does_username_exist(self):
        #open file/chck if username is in that file, return dic['hashed_password']
        hashed_password = ''
        event_type = 'login_failed'
        path = str("{username}.log")
        fl = File_handler(path)
        user_pass_list = fl.read()
        if self.username in user_pass_list:
            hashed_password = hashlib.sha512((self.password + Login.salt).encode()).hexdigest()
            event_type = 'login_successfull'
        self.log = Log_handler.log_handler(self.username,datetime.now(),event_type)
        return hashed_password

    def is_password_correct(self):
        hashed_password = self.does_username_exist()
        print(hashed_password)
        if hashed_password!=''and hashed_password == self.hashed_password:
            self.token = 'valid'
        else:
            self.log = Log_handler.log_handler(self.username, datetime.now(), 'login_failed')
        return self.token

a = Login('narges', '11a1')
print(a.is_password_correct())