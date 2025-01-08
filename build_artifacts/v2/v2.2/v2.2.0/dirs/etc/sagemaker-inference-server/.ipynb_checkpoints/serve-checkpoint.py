from __future__ import absolute_import

from tornado_server.server import TornadoServer


if __name__ == "__main__":
    inference_server = TornadoServer()
    inference_server.serve()
