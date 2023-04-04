from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


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

if __name__ == "__main__":
    handler = MyFTPHandler

    authorizer = DummyAuthorizer()
    authorizer.add_user("epsi", "client22", "./home/epsi", perm="elradfmwMT")
    authorizer.add_anonymous("./home/epsi")

    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()
    print("toto")
    # Kill serveur

    server.close_all()
    print("rallumé")
    # Allumer serveur

    server.serve_forever()

