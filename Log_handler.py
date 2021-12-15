import datetime
import logging
from File_handler_module import File_Handler

class Log_handler:

    system_log = 'system_log.log'
    def __init__(self,username, time,event_type):
        self.time =time
        self.event_type = event_type

    @classmethod
    def log_handler(cls,username, time,event_type):
        path = "username_password.csv"
        fl = File_Handler(path)
        user_pass_list = fl.read()
        log_path = ''
        for elem in user_pass_list:
            if username == elem['username']:
                a = cls(username, time,event_type)
                log_path = "{0}.log".format(username)
        else:
            a = Log_handler(cls.system_log, time, event_type)
            log_path = f"{cls.system_log}.log"
        # logging.log(time=time,path=log_path,event_type=event_type,level=logging.INFO,msg="")

log_path = "system_log.log"
event_type="login_failed"
time = datetime.datetime.now()
