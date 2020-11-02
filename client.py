import socket
from _thread import *
import threading
import os
import time
import sys


HOST = 'localhost'              # github : lubnc4261
PORT = 33000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)
CONNECTED = True


CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def clear():

    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def connect_to_server(count):
    connected = False
    try:
        CLIENT.connect(ADDR)
        connected = True
    except:
        if count != 6:
            print("[*] Could not connect to the Server, Try {}/5\n".format(count))
            count += 1
            time.sleep(1)
            connect_to_server(count)
        else:
            print('[*] Could not contact the Server at this time.\n[*] The server may be offline or down for maintenance\n[*] Sorry for the inconvenience.')
            os.sys.exit()

    if connected:
        print("[*] Connected to the Server.")
        print("[*] Creator : (github) lubnc4261 (lucas EF)")
        input('[*] Press enter to continue...')
        RECEIVE_THREAD = threading.Thread(target=receive)
        RECEIVE_THREAD.start()

def receive():
    if CONNECTED:
        MESSAGE_LOG = ''
        SEND_THREAD = threading.Thread(target=send_msg)
        SEND_THREAD.start()
        while True:
            try:
                message = CLIENT.recv(BUFFER_SIZE).decode()
                MESSAGE_LOG += message
                if message != '<quit>':
                    clear()
                    print(MESSAGE_LOG)
                else:
                    CLIENT.close()
                    break
            except OSError:
                break
    else:
        pass
def send_msg():
    while True:
        message = input("-> ")
        try:
            if message != '<quit>':
                CLIENT.send(message.encode())
            else:
                CLIENT.send(message.encode())
                break
        except:
            print("Connection to server lost")
            break
def Main():
    clear()
    connect_to_server(1)

if __name__ == '__main__':
    Main()

sys.stdout.write("\x1b]2;Viper Client\x07")
