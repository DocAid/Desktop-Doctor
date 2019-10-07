import socket
import requests
import json
import pickle

HEADERSIZE = 10



def server_program():
    # get the hostname
    # host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(('localhost', port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    clientsocket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    data = clientsocket.recv(1024).decode()
    print(str(data))
    print(data.decode())

    clientsocket.close()
if __name__ == '__main__':
    server_program()