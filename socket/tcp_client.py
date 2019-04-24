import socket
import threading
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")


class TcpClient:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.raddr = (ip, port)
        self.sock = socket.socket()
        self.event = threading.Event()

    def start(self):
        self.sock.connect(self.raddr)
        self.send('client connect')
        threading.Thread(target=self.recv, name='recv').start()

    def stop(self):
        self.sock.close()
        self.event.wait(3)
        self.event.set()
        logging.info('client stop')

    def send(self, data: str):
        data = "{}\n".format(data).encode()
        self.sock.send(data)

    def recv(self):
        while not self.event.is_set():
            try:
                data = self.sock.recv(1024)
            except Exception as e:
                logging.error(e)
                break
            msg = "{}:{}\n{}".format(*self.raddr, data.decode())
            logging.info(msg)


def main():
    cc = TcpClient()
    cc.start()
    while True:
        cmd = input('>>>:')
        if cmd.strip() == 'exit':
            cc.stop()
            break
        cc.send(cmd)


if __name__ == '__main__':
    main()
