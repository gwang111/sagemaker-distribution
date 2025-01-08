from __future__ import absolute_import

import asyncio
import logging
import tornado.web
from utils.environment import Environment
from utils.exception import SyncInvocationsException
from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER
from typing import Generator

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class InvocationsHandler(tornado.web.RequestHandler):
    def initialize(self, handler: callable, environment: Environment):
        self._handler = handler
        self._environment = environment

    async def post(self):
        try:
            response = await IOLoop.current().run_in_executor(None, self._handler, self.request)
            self.write(response)    
        except Exception as e:
            raise SyncInvocationsException(e)


class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")


async def serve(handler: callable, environment: Environment):
    logger.info("Starting inference server in synchronous mode...")

    app = tornado.web.Application([
        (r"/invocations", InvocationsHandler, dict(handler=handler, environment=environment)),
        (r"/ping", PingHandler),
    ])
    app.listen(environment.port)
    logger.debug(f"Synchronous inference server listening on port: `{environment.port}`")
    await asyncio.Event().wait()
