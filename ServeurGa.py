from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import tftpy
from multiprocessing import Process

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

class CustomTftpServer(tftpy.TftpServer):
    def __init__(self, root, handler=None):
        super().__init__(root, handler)
        self.FTPserveur = Process(target=serverFTP)

    def handle(self, request, handler):
        self.before_connection(request)  # Exécutez la fonction avant la connexion
        super().handle(request, handler)
        self.after_connection(request)   # Exécutez la fonction après la connexion

    def before_connection(self, request):
        print("Avant la connexion:", request)

    def after_connection(self, request):
        self.FTPserveur.terminate()
        self.FTPserveur.join()
        self.FTPserveur = Process(target=serverFTP)
        self.FTPserveur.start()


def serverFTP():
    handler = MyFTPHandler

    mdp = lectureMDP()

    authorizer = DummyAuthorizer()
    authorizer.add_user("epsi", mdp, "./home/epsi", perm="elradfmwMT")
