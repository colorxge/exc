from socketserver import ThreadingTCPServer, BaseRequestHandler
import threading
import sys
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(thread)d %(message)s")


class ChatHandler(BaseRequestHandler):
    clients = {}

    def setup(self):   # 初始工作
        super().setup()
        self.event = threading.Event()  
        self.clients[self.client_address] = self.request

    def finish(self):   # 清理工作
        super().finish()    
        self.clients.pop(self.client_address)
        self.event.set()

    def handle(self):
        super().handle()

        while not self.event.is_set():
            data = self.request.recv(1024).decode()
            print(data, '~~~~~~') # 增加
            if not data or data == 'quit':
                break
            msg = "{} {}".format(self.client_address, data).encode()
            logging.info(msg)
            for c in self.clients.values():
                print('+++++++')
                c.send(msg)
        print('End')


addr = ('0.0.0.0', 9999)
server = ThreadingTCPServer(addr, ChatHandler)

server_thread = threading.Thread(target=server.serve_forever, name='ChatServer', daemon=True)
server_thread.start()

try:
    while True:
        cmd = input(">>>")
        if cmd.strip() == 'quit':
            server.shutdown()
            break
        print(threading.enumerate())
except Exception as e:
    print(e)
except KeyboardInterrupt:
    pass
finally:
    print('Exit')
    sys.exit(0)
