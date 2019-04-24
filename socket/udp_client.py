import socket
import threading
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")


class UdpClient:
    def __init__(self, rip='127.0.0.1', rport=9999):
        self.raddr = (rip, rport)
        self.sock = socket.socket(type=socket)
        self.event = threading.Event()

    def start(self):
        self.sock.connect(self.raddr)   # 占用本地地址和端口，设置远端地址和端口
        threading.Thread(target=self._sendhb, name='heartbeat', daemon=True).start()
        threading.Thread(target=self.recv, name='recv').start()

    def _sendhb(self):
        while not self.event.wait(5):
            self.sendto('^hb^')

    def recv(self):
        while not self.event.is_set():
            data ,raddr = self.sock.recvfrom(1024)
            msg = '{}. from {}:{}'.format(data.decode(), *raddr)
            logging.info(msg)

    def sendto(self, msg: str):
        self.sock.sendto(msg.encode(), self.raddr)

    def stop(self):
        self.sendto('quit')
        self.sock.close()
        self.event.set()


if __name__ == '__main__':
    c1 = UdpClient()
    c2 = UdpClient()
    c1.start()
    c2.start()
    print(c1.sock)
    print(c2.sock)

    while True:
        cmd = input('Input your words >>')
        if cmd.strip() =='quit':
            c1.stop()
            c2.stop()
            break
        c1.sendto(cmd)
        c2.sendto(cmd)

