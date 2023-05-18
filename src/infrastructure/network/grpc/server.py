from domain.event import Event
from domain.git.git_repo_found import GitRepoFound
from domain.primary_port import PrimaryPort

import infrastructure.network.grpc.git_repo_found_pb2 as git_repo_found_pb2
import infrastructure.network.grpc.git_repo_found_pb2_grpc as git_repo_found_pb2_grpc

from concurrent import futures
import grpc

import asyncio
import time
import json
import logging
from typing import Dict

class Server(PrimaryPort, git_repo_found_pb2_grpc.GitRepoFoundServiceServicer):

    """
    Launches a gRPC server to receive incoming events.
    """
    def priority(self) -> int:
        return 999

    @property
    def app(app):
        return self._app

    async def GitRepoFoundNotifications(self, request, context):
        logging.getLogger(__name__).debug(f'Received "{request}", "{context}"')
        response = git_repo_found_pb2.Reply(code=200)
        event = self.build_event(request)
        await self._app.accept(event)
        return response

    async def serve(self, app):
        server = grpc.aio.server()
        git_repo_found_pb2_grpc.add_GitRepoFoundServiceServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        logging.getLogger(__name__).info(f'gRPC server listening at port 50051')
        await server.start()
        await server.wait_for_termination()
#
    async def accept(self, app):
        self._app = app
        serve_task = asyncio.create_task(self.serve(app))
        asyncio.ensure_future(serve_task)
        try:
            await serve_task
        except KeyboardInterrupt:
            serve_task.cancel()
            try:
                await serve_task
            except asyncio.CancelledError:
                pass

    def build_event(self, request) -> Event:
        return GitRepoFound(request.package_name, request.package_version, request.url, request.tag)
