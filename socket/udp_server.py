import socket
import threading
import logging
import datetime
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")


class UdpServer:
    def __init__(self, ip='127.0.0.1', port=9999, interval=10):
        self.addr = (ip, port)
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()
        self.clients = {} # 记录客户端
        self.interval = interval  # 心跳检测间隔时间，超时移除客户端

    def start(self):
        self.sock.bind(self.addr)   # 绑定
        threading.Thread(target=self.recvfrom).start()  # 启动线程

    def recvfrom(self):
        while not self.event.is_set():
            localset = set()    # 清理超时
            data, client = self.sock.recvfrom(1024)    # 等待阻塞

            current = datetime.datetime.now().timestamp() # float
            if data.strip() == b'^hb^':
                print('^^^^hb', client)
                self.clients[client] = current
            elif data.strip() == b'quit':
                # 有可能发来的数据不再client中
                self.clients.pop(client, None)
                logging.info('{} leaving'.format(client))

            # 有消息来就更新时间， 发消息时判断时间有没有超时
            self.clients[client] = current

            msg = "{}:{}\n{}".format(*client, data)
            logging.info(msg)
            msg = msg.encode()

            for client, stamp in self.clients.items():
                if current - stamp > self.interval:
                    localset.add(client)
                else:
                    self.sock.sendto(msg, client)
            [self.clients.pop(c) for c in localset]

    def sendto(self, data: str, addr):
        data = data.encode()
        self.sock.sendto(data, addr)

    def stop(self):
        for client in self.clients:
            msg = "{}:zhe server off".format(self.addr)
            self.sendto(msg, client)
        self.sock.close()
        self.event.set()


if __name__ == '__main__':
    cs = UdpServer()
    cs.start()
    while True:
        cmd = input(">>>:")
        if cmd.strip() == 'quit':
            cs.stop()
            break
        logging.info(threading.enumerate())
        logging.info(cs.clients)

