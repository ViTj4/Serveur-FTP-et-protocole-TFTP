from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer

class MyFTPHandler(FTPHandler):
    authorizer = DummyAuthorizer()
    authorizer.add_user("epsi", "client22", "/path/to/home", perm="elradfmwMT")
    authorizer.add_anonymous("/path/to/public")

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

handler = MyFTPHandler()
handler.authorizer = MyFTPHandler.authorizer
handler.banner = "Welcome to my FTP server"
handler.passive_ports = range(60000, 65535)
handler.timeout = 600

server = FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()
