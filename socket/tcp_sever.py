import socket
import threading
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")


class SocketServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.sock = socket.socket()
        self.addr = (ip, port)
        self.clients = {}
        self.event = threading.Event()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        threading.Thread(target=self.accept, name='accept').start()

    def stop(self):
        for sock in self.clients.values():
            sock.close()
        self.event.set()
        self.sock.close()

    def accept(self):
        while not self.event.is_set():
            sock, raddr = self.sock.accept()
            self.clients[raddr] = sock
            threading.Thread(target=self.recv, args=(sock, raddr), name='recv').start()

    def recv(self, sock: socket, raddr):
        while not self.event.is_set():
            try:
                data = sock.recv(1024)
            except Exception as e:
                logging.info(e)
                break
            if data.strip() == b'quit':
                sock.send(b'close')
                self.clients.pop(raddr)
                break
            msg = "{}:{}\n{}".format(*raddr, data.decode())
            logging.info(msg)
            msg = msg.encode()
            [client.send(msg) for client in self.clients.values()]

    def send(self, data: str, sock):
        data = data.encode()
        sock.send(data)


server = SocketServer()
server.start()


while True:
    a = input('>>>:')
    if a == 'exit':
        break




