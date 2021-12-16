import csv

class File_Handler:
    def __init__(self, path):
        self.path = path
    def read(self):
        list_content=[]
        try:
            with open(self.path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                list_content = [item for item in csv_reader]#list(csv_reader)
        except Exception as ex:
            print(ex)
        return list_content

    def write(self, kwargs):

        try:
            with open(self.path, 'a', newline='') as csvfile:

                fieldnames = list(kwargs.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if len(open(self.path).readlines())== 0:
                    writer.writeheader()
                writer.writerow(kwargs)
        except Exception as ex:
            print(ex.with_traceback())

        return

def debugger(fun):
    def wrapper(*args , **kwargs):
        print(fun.__name__)
        print("arguments: ",args if len(args)>0 else"" , kwargs if len(kwargs)>0 else"")



