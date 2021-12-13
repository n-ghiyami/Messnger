import logging
import File_handler

class Log_handler:

    system_log = 'system_log.log'
    def __init__(self,username, time,event_type):
        self.time =time
        self.event_type = event_type

    @classmethod
    def log_handler(cls,username, time,event_type):
        path = "username_password.csv"
        fl = File_handler(path)
        user_pass_list = fl.read()
        log_path = ''
        if username in user_pass_list['userame']:
            a = cls(username, time,event_type)
            log_path = f"{username}.log"
        else:
            a = Log_handler(cls.system_log, time, event_type)
            log_path = f"{cls.system_log}.log"
        logging.log(time=time,path=log_path,event_type=event_type)
