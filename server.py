# -*- coding: utf-8 -*-

import socket
import sys

ip = (sys.argv[1])
port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(True)
server.bind((ip, port))
server.listen(1)

print 'Aguardando pela conexão da urna...'
connection, client_address = server.accept()
print 'Conexão estabelecida!'

while True:

    #receive file name
    file_name = connection.recv(1024).split(';-;-')[0]

    if(file_name == 'EOFCLOSE'):
        break

    #receive file size
    file_size = int(connection.recv(1024).split(';-;-')[0])

    #print file_name," - ",file_size

    #file chunks
    file_chunks = file_size / 1024

    #rest
    rest = file_size - (file_chunks * 1024)

    #print "Chunks: ", file_chunks
    #print "Rest: ", rest

    file = ''

    for i in range(file_chunks):
        file += connection.recv(1024)

    if(rest > 0):
        file += connection.recv(rest)

    with open(file_name, 'w') as out:
        out.write(file)

    print 'Boleta recebida com sucesso!'

connection.close()
server.close()