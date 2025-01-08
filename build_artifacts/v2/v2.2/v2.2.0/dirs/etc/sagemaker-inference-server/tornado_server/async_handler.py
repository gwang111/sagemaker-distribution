from __future__ import absolute_import

import asyncio
import logging
import tornado.web
from utils.environment import Environment
from utils.exception import AsyncInvocationsException
from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class InvocationsHandler(tornado.web.RequestHandler):
    def initialize(self, handler: callable, environment: Environment):
        self._handler = handler
        self._environment = environment

    async def post(self):
        try:
            response = await self._handler(self.request)
            self.write(response)
        except Exception as e:
            raise AsyncInvocationsException(e)


class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")


async def serve(handler: callable, environment: Environment):
    logger.info("Starting inference server in asynchronous mode...")

    app = tornado.web.Application([
        (r"/invocations", InvocationsHandler, dict(handler=handler, environment=environment)),
        (r"/ping", PingHandler),
    ])
    app.listen(environment.port)
    logger.debug(f"Asynchronous inference server listening on port: `{environment.port}`")
    await asyncio.Event().wait()
