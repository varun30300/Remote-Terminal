from pydoc import cli
from select import select
import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path


def get_working_directory_info(working_directory): # done, do not touch 
    """
    Creates a string representation of a working directory and its contents.
    :param working_directory: path to the directory
    :return: string of the directory and its contents.
    """
    dirs = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_dir()])
    files = '\n-- ' + '\n-- '.join([i.name for i in Path(working_directory).iterdir() if i.is_file()])
    dir_info = f'Current Directory: {working_directory}:\n|{dirs}{files}'
    return dir_info


def generate_random_eof_token(): # done, do not touch
    """Helper method to generates a random token that starts with '<' and ends with '>'.
     The total length of the token (including '<' and '>') should be 10.
     Examples: '<1f56xc5d>', '<KfOVnVMV>'
     return: the generated token.
     """
    collection = []
    for x in range(48,58):
        collection.append(x)
    for x in range(65,91):
        collection.append(x)
    for x in range(97,123):
        collection.append(x)

    eof = random.choices(collection,k=8)
    eof = "<"+"".join([chr(i) for i in eof])+">"
    return eof
    #raise NotImplementedError('Your implementation here.')

def receive_message_ending_with_token(active_socket, buffer_size, eof_token): # done, do not touch
    """
    Same implementation as in receive_message_ending_with_token() in client.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
    """
    # raise NotImplementedError('Your implementation here.')

    client_content = bytearray()

    while True:
        packet = active_socket.recv(buffer_size)
        if packet[-10:] == eof_token.encode():
            client_content += packet[:-10]
            break
        client_content += packet
    return client_content


def handle_cd(current_working_directory, new_working_directory): #done , do not touch 
    """
    Handles the client cd commands. Reads the client command and changes the current_working_directory variable 
    accordingly. Returns the absolute path of the new current working directory.
    :param current_working_directory: string of current working directory
    :param new_working_directory: name of the sub directory or '..' for parent
    :return: absolute path of new current working directory
    """
    # raise NotImplementedError('Your implementation here.')
    os.chdir(new_working_directory)
    current_working_directory = os.getcwd()
    return current_working_directory


def handle_mkdir(current_working_directory, directory_name): #done , do not touch 
    """
    Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
    :param current_working_directory: string of current working directory
    :param directory_name: name of new sub directory
    """
    # raise NotImplementedError('Your implementation here.')
    os.mkdir(directory_name)
    current_working_directory = os.getcwd()
    return current_working_directory


def handle_rm(current_working_directory, object_name): #done , do not touch 
    """ 
    Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
    based on the object type (directory/file).
    :param current_working_directory: string of current working directory
    :param object_name: name of sub directory or file to remove
    """
    # raise NotImplementedError('Your implementation here.')
    if '.' in object_name:
        os.remove(object_name)
    else:
        os.rmdir(object_name)
    current_working_directory = os.getcwd()
    return current_working_directory


def handle_ul(current_working_directory, file_name, service_socket, eof_token): # done, do not touch
    """
    Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
    file in the current working directory.
    Use the helper method: receive_message_ending_with_token() to receive the message from the client.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be created.
    :param service_socket: active socket with the client to read the payload/contents from.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
   
    new_file = open(file_name, "wb")
    # data = service_socket.recv(1024).decode()
    data = receive_message_ending_with_token(service_socket, 1024, eof_token)
    new_file.write(data)
    new_file.close()
    current_working_directory = os.getcwd()
    return current_working_directory
   
    # print("UL end - ",current_working_directory)
    # return current_working_directory

def handle_dl(current_working_directory, file_name, service_socket, eof_token):
    """
    Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
    given socket.
    :param current_working_directory: string of current working directory
    :param file_name: name of the file to be sent to client
    :param service_socket: active service socket with the client
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
    file = open(file_name,"rb")
    data = file.read() + eof_token.encode()
    service_socket.send(data)
    file.close()
    current_working_directory = os.getcwd()
    return current_working_directory

class ClientThread(Thread):
    def __init__(self, service_socket : socket.socket, address : str):
        Thread.__init__(self)
        self.service_socket = service_socket
        self.address = address

    def run(self):
        print ("Connection from : ", self.address)
        # raise NotImplementedError('Your implementation here.')

        # initialize the connection
        # conn, addr = self.service_socket.accept()

        # send random eof token
        eof = generate_random_eof_token()
        print("EOF is : ", eof)
        self.service_socket.send(eof.encode())

        # establish working directory
        cwd = os.getcwd()
        # send the current dir info
        self.service_socket.send(get_working_directory_info(cwd).encode())

        while True:
            # print("Server loop start")
        #   get the command and arguments and call the corresponding method
            cmd_eof = self.service_socket.recv(1024).decode()
            cmd = cmd_eof[:-10]
            eof = cmd_eof[-10:]
            # print("CMD is : ", cmd)
            

            if (cmd[0:2] == "cd"):
                newDir = handle_cd(cwd,cmd.split(" ")[1])
                # print("New dir : ", newDir)
                self.service_socket.send(get_working_directory_info(newDir).encode())

            elif (cmd[0:5] == "mkdir"):
                newDir = handle_mkdir(cwd,cmd.split(" ")[1])
                # print("New dir : ", newDir)
                # send current dir info
                self.service_socket.send(get_working_directory_info(newDir).encode())
            
            elif (cmd[0:2] == "rm"):
                newDir = handle_rm(cwd,cmd.split(" ")[1])
                # print("New dir : ", newDir)
                # send current dir info
                self.service_socket.send(get_working_directory_info(newDir).encode())

            elif (cmd[0:2] == "ul"):
                newDir = handle_ul(cwd,cmd.split(" ")[1],self.service_socket,eof)
                # print("New dir : ", newDir)
                # send current dir info
                self.service_socket.send(get_working_directory_info(newDir).encode())

            elif (cmd[0:2] == "dl"):
                newDir = handle_dl(cwd,cmd.split(" ")[1],self.service_socket,eof)
                # print("New dir : ", newDir)
                # send current dir info
                self.service_socket.send(get_working_directory_info(newDir).encode())


        # print('Connection closed from:', self.address)

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn,addr = s.accept()
            client_thread = ClientThread(conn,addr)
            client_thread.start()

if __name__ == '__main__':
    main()


