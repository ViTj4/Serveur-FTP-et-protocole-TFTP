import os
import sys
from multiprocessing import Process
from pyftpdlib.authorizers import DummyAuthorizer
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


def get_password():
    try:
        with open(PASSWORD_FILE, "r") as f:
            return f.readline().strip()
    except:
        return FTP_PASSWORD


def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, get_password(), FTP_DIRECTORY, perm='elradfmw')
    authorizer.add_anonymous(os.getcwd())

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."
    # handler.passive_ports = range(60000, 65535)

    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    tftp_root = "./secret"
    server = CustomTftpServer(tftp_root)
    server.FTPserveur.start()

def start_tftp_server():
    # Prompt the user to enter a new password.
    new_password = input("Enter new password: ")

    # Write the new password to the password file.
    with open("password.txt", "w") as f:
        f.write(new_password)

    try:
        os.chmod(FTP_DIRECTORY, 0o777)
    except Exception as e:
        print(f"Failed to change permissions of {FTP_DIRECTORY}: {str(e)}")

    try:
        server = TftpServer(FTP_DIRECTORY)
        # server.listen()
        p = Process(target=start_ftp_server)
        p.start()  # Démarrage du serveur FTP dans un processus séparé
        p.join()  # Attendre que le processus soit terminé avant de continuer
    except FilesystemError as e:
        print(f"Failed to start TFTP server: {str(e)}")


def main():
    print("Choose an option:")
    print("1. Start FTP server")
    print("2. Start TFTP server to change client's password")

    choice = input("Enter 1 or 2: ")
    if choice == "1":
        start_ftp_server()
    elif choice == "2":
        start_tftp_server()
    else:
        print("Invalid choice")
        sys.exit(1)


if __name__ == '__main__':
    main()