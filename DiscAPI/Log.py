from datetime import timedelta

class Log:
    def Debug(client, Content):
        if client.Log == True:
            time = client.uptime / 24 / 60 / 60
            print(bc.LOG+"[Log][{}] {}".format(str(timedelta(time)), Content) + bc.END)

    def Warning(Content):
        print(Content)
    
    def Error(Content):
        print(Content)
    
class bc:
    LOG = '\033[90m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
