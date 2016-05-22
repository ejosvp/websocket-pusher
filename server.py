import socket
import sys

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver
import tornado.websocket
import tornado.httpserver
import tornado.web

clients = []


class SimpleTcpClient:
    client_id = 0

    def __init__(self, stream):
        SimpleTcpClient.client_id += 1
        self.id = SimpleTcpClient.client_id
        self.stream = stream

        self.stream.socket.setsockopt(
            socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.stream.socket.setsockopt(
            socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        self.stream.set_close_callback(self.on_disconnect)

    @tornado.gen.coroutine
    def on_disconnect(self):
        yield []

    @tornado.gen.coroutine
    def dispatch_client(self):
        try:
            while True:
                line = yield self.stream.read_until(b'\n')
                message = line.decode('utf-8').strip()
                for client in clients:
                    client.write_message(message)
                yield self.stream.write(line)
        except tornado.iostream.StreamClosedError:
            pass

    @tornado.gen.coroutine
    def on_connect(self):
        yield self.dispatch_client()


class SimpleTcpServer(tornado.tcpserver.TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        connection = SimpleTcpClient(stream)
        yield connection.on_connect()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clients:
            clients.append(self)

    def on_close(self):
        if self in clients:
            clients.remove(self)

    def on_message(self, message):
        for client in clients:
            if client != self:
                client.write_message(message)


def main():
    # configuration
    host = sys.argv[1]
    port = int(sys.argv[2])
    loop = tornado.ioloop.IOLoop.instance()

    # webSocket server
    app = tornado.web.Application([
        (r'/', WebSocketHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(app, io_loop=loop, ssl_options={
        'certfile': 'server.crt',
        'keyfile': 'server.key'
    })

    http_server.listen(port, host)

    # tcp server
    tcp_server = SimpleTcpServer(io_loop=loop)
    tcp_server.listen(port + 1, host)

    # infinite loop
    loop.start()


if __name__ == '__main__':
    main()
