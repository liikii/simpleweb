"""
auth: liikii.
"""
from json import loads
import signal
import logging
import sys

from tornado.websocket import websocket_connect
from tornado import web, gen, ioloop, websocket


logger = logging.getLogger('simple_task')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('simple_task.log')
fh.setLevel(logging.DEBUG)

fmt = '%(asctime)s - %(name)s - %(levelname)s \n%(message)s\n'
formatter = logging.Formatter(fmt)
fh.setFormatter(formatter)

logger.addHandler(fh)


def signal_handler(signum, frame):
    # catch the terminal stop/kill signal.close the IOLoop
    ioloop.IOLoop.instance().stop()
    sys.stdout.write("\n\n  --- exit successfully, bye ---  \n\n")
    sys.exit(0)


class WebSocketHandler(websocket.WebSocketHandler):
    clt_s = set()
    # csz = 108
    msg = []

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.host = None

    @classmethod
    def send_updates(cls, chat):
        for clt in cls.clt_s:
            try:
                clt.write_message(chat)
            except:
                logger.error("Error sending message", exc_info=True)

    @gen.coroutine
    def open(self):
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        self.host = remote_ip
        logger.info('log in %s ' % remote_ip)
        WebSocketHandler.clt_s.add(self)
        if len(WebSocketHandler.clt_s) > 200:
            WebSocketHandler.clt_s.pop()
        for m in WebSocketHandler.msg:
            self.write_message(m)

    @gen.coroutine
    def on_message(self, message):
        print('ws', message)
        logger.info('task : %s ' % message)
        WebSocketHandler.send_updates(message)
        WebSocketHandler.msg.append(message)
        if len(WebSocketHandler.msg) > 200:
            WebSocketHandler.msg.pop(0)

    def on_close(self):
        print('close')
        logger.info('log out %s ' % self.host)
        WebSocketHandler.clt_s.remove(self)


class IdxHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        # web.StaticFileHandler, {"path": './static', "default_filename": "haha4.html"}
        f = open('./static/haha4.html', 'r', encoding='utf8')
        d = f.read()
        f.close()
        self.write(d)
        return

    @gen.coroutine
    def post(self):
        return


class MainHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        return

    @gen.coroutine
    def post(self):
        bdy = self.request.body
        ubd = bdy.decode('utf-8')
        dt = loads(ubd)
        self.set_status(200, 'ok.')
        self.write('{}')

        ws = yield websocket_connect('ws://127.0.0.1:8666/ws')
        ws.write_message(ubd)
        return


def make_app():
    return web.Application([
        (r'/favicon.ico', MainHandler),
        (r'/haha', MainHandler),
        (r'/?', IdxHandler),
        (r'/ws', WebSocketHandler),
        (r'/s/(.*)', web.StaticFileHandler, {"path": './static'})
    ], autoreload=True)


# curl -vX POST http://127.0.0.1:8666/haha -d @haha17.txt --header "Content-Type: application/json"
if __name__ == "__main__":
    # for linux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    app = make_app()
    app.listen(8666)
    ioloop.IOLoop.current().start()
