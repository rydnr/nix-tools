from domain.event import Event
from domain.git_repo_found import GitRepoFound
from domain.primary_port import PrimaryPort

from concurrent import futures
import grpc
import hello_pb2
import hello_pb2_grpc

import asyncio
import time
import json
import logging
from typing import Dict

class Server(PrimaryPort, hello_pb2_grpc.GreeterServicer):

    """
    Launches a gRPC server to receive incoming events.
    """
    def priority(self) -> int:
        return 100

    @property
    def app(app):
        return self._app

    async def SayHello(self, request, context):
        logging.getLogger(__name__).debug(f'Received "{request}", "{context}"')
        response = hello_pb2.HelloReply(message='Hello, %s!' % request.name)
        event = self.build_event(request)
        await self._app.accept(event)
        return response

    async def serve(self, app):
        server = grpc.aio.server()
        hello_pb2_grpc.add_GreeterServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        logging.getLogger(__name__).info(f'gRPC server listening at port 50051')
        await server.start()
        await server.wait_for_termination()
#
    async def accept(self, app):
        self._app = app
        serve_task = asyncio.create_task(self.serve(app))
        asyncio.ensure_future(serve_task)

    def build_event(self, request) -> Event:
        return GitRepoFound("beautifulsoup4", "4.1.3", "https://git.launchpad.net/beautifulsoup", "4.1.3")
