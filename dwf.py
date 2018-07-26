#!/usr/local/bin/python3
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

print(9000)
r = File('.', ignoredExts=('.py'))
factory = Site(r)
reactor.listenTCP(9000, factory)
reactor.run()

