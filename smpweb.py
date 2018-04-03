from tornado import web, gen, ioloop
from json import loads


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


class MHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        return

    @gen.coroutine
    def post(self):
        bdy = self.request.body
        dt = loads(bdy.decode('utf-8'))
        self.set_status(404, 'ddd')
        self.write('{}')
        return


def make_app():
    return web.Application([
        (r'/favicon.ico', MHandler),
        (r'/haha', MHandler),
        (r'/?', IdxHandler),
        (r'/s/(.*)', web.StaticFileHandler, {"path": './static'})
    ], autoreload=True)


# curl -vX POST http://127.0.0.1:8666/haha -d @haha17.txt --header "Content-Type: application/json"
if __name__ == "__main__":
    app = make_app()
    app.listen(8666)
    ioloop.IOLoop.current().start()
