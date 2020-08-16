import socket

HOST = 'localhost'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        print('Enter Message. To quit(q)')
        message = input()
        if message == 'q': break
        s.sendall(bytes(message, 'utf-8'))
        data = s.recv(1024)
        print('Received', str(data))