from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import tftpy
from multiprocessing import Process
import time

class MyFTPHandler(FTPHandler):

    def on_connect(self):
        print(f"Client {self.remote_ip} connected")

    def on_disconnect(self):
        print(f"Client {self.remote_ip} disconnected")

    def on_login(self, username):
        print(f"User {username} logged in")

    def on_logout(self, username):
        print(f"User {username} logged out")

    def on_file_sent(self, file):
        print(f"File {file} sent")

    def on_file_received(self, file):
        print(f"File {file} received")

def lectureMDP():
    with open('./secret/pwd.txt') as secret:
        mdp = secret.readline()
    return mdp


def serverFTP():
    handler = MyFTPHandler

    mdp = lectureMDP()

    authorizer = DummyAuthorizer()
    authorizer.add_user("epsi", mdp, "./home/epsi", perm="elradfmwMT")

    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()

def serverTFTP():
    tftp_root = "./secret"
    server = tftpy.TftpServer(tftp_root)

    server.listen("127.0.0.1", 69)

if __name__ == "__main__":
    FTPserveur = Process(target=serverFTP)
    TFTPserveur = Process(target=serverTFTP)   
    true_mdp = lectureMDP()
    FTPserveur.start()
    TFTPserveur.start()
    while True:
        time.sleep(5)
        mdp = lectureMDP()
        if true_mdp != mdp:
            FTPserveur.terminate()
            FTPserveur.join()
            FTPserveur = Process(target=serverFTP)
            FTPserveur.start()
            true_mdp = mdp
