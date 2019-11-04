import time
#from AutoTestLibSIT import *

def sms(msg):
    C = socket(AF_INET, SOCK_STREAM)
    print(msg)
    C.connect(('192.168.100.80', 22009))
    C.send(msg)


if __name__ == '__main__':
    if not 5:print('ddd')
