import socket

def receive_message_ending_with_token(active_socket, buffer_size, eof_token): # done, do not touch
    """
    Same implementation as in receive_message_ending_with_token() in server.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
    """
    # raise NotImplementedError('Your implementation here.')
    server_content = bytearray()

    while True:
        packet = active_socket.recv(buffer_size)
        if packet[-10:] == eof_token.encode():
            server_content += packet[:-10]
            break
        server_content += packet
    return server_content


def initialize(host, port): # done, do not touch
    """
    1) Creates a socket object and connects to the server.
    2) receives the random token (10 bytes) used to indicate end of messages.
    3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param host: the ip address of the server
    :param port: the port number of the server
    :return: the created socket object
    """
    # raise NotImplementedError('Your implementation here.')

    # Creates a socket object and connects to the server.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    print('Connected to server at IP:', host, 'and Port:', port)

    # receives the random token (10 bytes) used to indicate end of messages.
    global eof_token 
    eof_token = s.recv(1024).decode()
    print('Handshake Done. EOF is:', eof_token)

    #Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
    iniWD = s.recv(1024).decode()
    print(iniWD)
    
    return s


def issue_cd(command_and_arg, client_socket, eof_token):
    """
    Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
    command_and_arg_and_eof = command_and_arg + eof_token
    client_socket.send(command_and_arg_and_eof.encode())
    cwd_info = client_socket.recv(1024).decode()
    print(cwd_info)
    # cd_cmd = receive_message_ending_with_token(client_socket, 1024 , eof_token)



def issue_mkdir(command_and_arg, client_socket, eof_token):
    """
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
    command_and_arg_and_eof = command_and_arg + eof_token
    client_socket.send(command_and_arg_and_eof.encode())
    cwd_info = client_socket.recv(1024).decode()
    print(cwd_info)


def issue_rm(command_and_arg, client_socket, eof_token):
    """
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
    command_and_arg_and_eof = command_and_arg + eof_token
    client_socket.send(command_and_arg_and_eof.encode())
    cwd_info = client_socket.recv(1024).decode()
    print(cwd_info)


def issue_ul(command_and_arg, client_socket, eof_token): # done, do not touch
    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    # raise NotImplementedError('Your implementation here.')
    command_and_arg_and_eof = command_and_arg + eof_token
    client_socket.send(command_and_arg_and_eof.encode())

    filename = command_and_arg.split()[1]
    file = open(filename,"rb")
    data = file.read() + eof_token.encode()
    client_socket.send(data)
    file.close()

    cwd_info = client_socket.recv(1024).decode()
    print(cwd_info)


def issue_dl(command_and_arg, client_socket, eof_token):
    """
    Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
    socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
    the server.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return:
    """
    # raise NotImplementedError('Your implementation here.')
    command_and_arg_and_eof = command_and_arg + eof_token
    client_socket.send(command_and_arg_and_eof.encode())

    file_name = command_and_arg.split()[1]
    new_file = open(file_name, "wb")
    data = receive_message_ending_with_token(client_socket, 1024, eof_token)
    new_file.write(data)
    new_file.close()

    cwd_info = client_socket.recv(1024).decode()
    print(cwd_info)

def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    # raise NotImplementedError('Your implementation here.')

    # initialize
    s = initialize(HOST,PORT)

    while True:
        # print("Client loop start")
        
        # get user input
        print("Input - ")
        cmd = input()
        # call the corresponding command function or exit

        if cmd == "exit":
            print("Program has ended")
            break

        elif cmd[:2] == "cd":
            issue_cd(cmd, s, eof_token)
            
        elif cmd[:5] == "mkdir":
            issue_mkdir(cmd, s, eof_token)
            

        elif cmd[:2] == "rm":
            issue_rm(cmd, s, eof_token)
            

        elif cmd[:2] == "ul":
            issue_ul(cmd,s,eof_token)
        
        elif cmd[:2] == "dl":
            issue_dl(cmd,s,eof_token)
            
    
    # print('Exiting the application.')


if __name__ == '__main__':
    main()