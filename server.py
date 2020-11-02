import socket
from _thread import *
import threading
import os
import time
import sys
import colorama
from colorama import Fore, Back, Style, init
init()

HOST = ''                   # github : lubnc4261
PORT = 33000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

CLIENTS = {}
ADDRESSES = {}

BANNER ='''
    Github : lubnc4261 (lucas EF)

    Server ready
                         ,
                        ,@,
                       ,@@@,
                      ,@@@@@,
               `@@@@@@@@@@@@@@@@@@@`
                 `@@@@@@@@@@@@@@@`
                   `@@@@@@@@@@@`
                  ,@@@@@@`@@@@@@,
                  @@@@`     `@@@@
                 ;@`           `@;

    type 'help' for commands
'''

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def accept_connections():
    MENU_THREAD = threading.Thread(target=server_cmds)
    MENU_THREAD.start()
    while True:
        client_socket, client_address = SERVER.accept()
        print("[*] {}:{} has connected.".format(client_address[0], client_address[1]))
        client_socket.send("[*] Hey! Welcome to Viper Chat Room !\n[*] Please enter your name to get started.".encode())
        ADDRESSES[client_socket] = client_address
        CLIENT_THREAD = threading.Thread(target=handle_client, args=(client_socket,))
        CLIENT_THREAD.start()

def handle_client(client):
    client_name = client.recv(BUFFER_SIZE).decode()
    client.send("\n[*] Welcome {}!\n[*] If you ever want to exit: type <quit> in the chat.".format(client_name).encode())
    message = "\n[*] {} Has joined the chat room!".format(client_name)
    broadcast(message)
    CLIENTS[client] = client_name
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode()
            if message != "<quit>":
                broadcast(message, "\n"+ client_name +': ')
            else:
                close_connection(client)
                break
        except:
            continue
def broadcast(message, prefix=''):
    try:
        for user in CLIENTS:
            user.send("{}{}".format(prefix, message).encode())
    except:
        pass

def close_connection(client, kicked=False):
    if not kicked:
        client.send("<quit>".encode())
        broadcast("\n[*] {} has left the chat room.".format(CLIENTS[client]))
        print('[*] Client: \'{}\' ~ {} : {} Has disconnected.'.format(CLIENTS[client], ADDRESSES[client][0], ADDRESSES[client][1]))
    else:
        print('[*] Client: \'{}\' ~ {} : {} Has been kicked.'.format(CLIENTS[client], ADDRESSES[client][0], ADDRESSES[client][1]))
    client.close()
    del ADDRESSES[client]
    del CLIENTS[client]

def server_cmds():
    while True:
        cmd = input('-> ')
        if cmd.lower() == 'help':
            print('[*] SAY - Broadcast a message to the chat room.')
            print('[*] CLS - Clear the screen.')
            print('[*] HELP - Provides Help information for Server Commands / this right here.')
            print('[*] KICK - Kick a client from the server / every client gets notified.')
            print('[*] LS - Lists the current connections / username / used port.')
        elif cmd.lower() == 'say':
            message = input('What would you like to broadcast?\n>> ')
            broadcast(message, "\nSERVER: ")
        elif cmd.lower() == 'cls':
            clear()
            print(BANNER)
        elif cmd.lower() == 'creator':
            print('Github : lubnc4261')
        elif cmd.lower() == 'ls':
            for client in ADDRESSES:
                try:
                    print('[*] Client: \'{}\' ~ {} : {}'.format(CLIENTS[client], ADDRESSES[client][0], ADDRESSES[client][1]))
                except:
                    print('[*] Connection: {} : {}'.format(ADDRESSES[client][0], ADDRESSES[client][1]))
        elif cmd.lower() == 'kick':
            print('[*] Enter username to kick from the chat?\n')
            i = 0
            connection = []
            for client in ADDRESSES:
                try:
                    print('[{}] {}'.format(i+1, CLIENTS[client]))
                    i += 1
                    connection.append(client)
                except:
                    continue
            kick = input('\n>> ')
            try:
                connection[int(kick)-1].send("\n[*] Sorry but you have been kicked from the server. \n[*] The Admin will have his reasons".encode())
                broadcast('\n[*] {} Has been kicked from the server!'.format(CLIENTS[connection[int(kick)-1]]))
                close_connection(connection[int(kick)-1], kicked=True)
            except:
                print("[*] Cannot close connection! Maybe retry ")
        elif cmd.lower() == 'quit':
            for client in ADDRESSES:
                try:
                    print('[*] Closing Client: \'{}\' ~ {} : {}'.format(CLIENTS[client], ADDRESSES[client][0], ADDRESSES[client][1]))
                except:
                    print('[*] Closing Connection: {} : {}'.format(ADDRESSES[client][0], ADDRESSES[client][1]))
                client.close()
            os._exit(1)
        elif cmd != '':
            print("[*] Not a valid server command")

def Main():
    SERVER.listen(5)
    ACCEPT_THREAD = threading.Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

if __name__ == '__main__':
    clear()
    print(BANNER)
    Main()

sys.stdout.write("\x1b]2;Viper Server\x07")
