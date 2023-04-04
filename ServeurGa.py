import os
import sys
from multiprocessing import Process
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import FilesystemError
from tftpy import TftpServer

FTP_PORT = 21
TFTP_PORT = 6969
FTP_USER = "epsi"
FTP_PASSWORD = "MotDePasse"
FTP_DIRECTORY = "./home/epsi" # Modification du chemin vers le dossier
PASSWORD_FILE = "nom de ton fichier"


def change_password(new_password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new_password)


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

    address = ('127.0.0.1', FTP_PORT)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()


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