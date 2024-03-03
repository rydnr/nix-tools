# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/network/grpc/server.py

This file defines the Server class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
        server.add_insecure_port("[::]:50051")
        logging.getLogger(__name__).info(f"gRPC server listening at port 50051")
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
        return GitRepoFound(
            request.package_name,
            request.package_version,
            request.url,
            request.tag,
            request.metadata,
            request.subfolder,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
