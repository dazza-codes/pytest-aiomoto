# Copyright 2019-2022 Darren Weber
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import functools
import threading
import time

import aiohttp

from pytest_aiomoto.moto_services import CONNECT_TIMEOUT
from pytest_aiomoto.moto_services import MotoService


class AioMotoService(MotoService):
    """Will Create AioMotoService.
    Service is ref-counted so there will only be one per process. Real Service will
    be returned by `__aenter__`."""

    def __call__(self, func):
        # override on this prevents any use of this class as a synchronous server
        async def wrapper(*args, **kwargs):
            await self._aio_start()
            try:
                result = await func(*args, **kwargs)
            finally:
                await self._aio_stop()
            return result

        functools.update_wrapper(wrapper, func)
        wrapper.__wrapped__ = func
        return wrapper

    async def __aenter__(self):
        svc = self._services.get(self._service_name)
        if svc is None:
            self._services[self._service_name] = self
            self._refcount = 1
            await self._aio_start()
            return self
        else:
            svc._refcount += 1
            return svc

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._refcount -= 1

        if self._socket:
            self._socket.close()
            self._socket = None

        if self._refcount == 0:
            await self._aio_stop()
            del self._services[self._service_name]

    async def _aio_start(self):
        self._thread = threading.Thread(target=self._server_entry, daemon=True)
        self._thread.start()

        async with aiohttp.ClientSession() as session:
            start = time.time()

            while time.time() - start < 10:
                if not self._thread.is_alive():
                    break

                try:
                    # we need to bypass the proxies due to monkeypatches
                    async with session.get(
                        self.endpoint_url + "/static", timeout=CONNECT_TIMEOUT
                    ):
                        pass
                    break
                except (asyncio.TimeoutError, aiohttp.ClientConnectionError):
                    await asyncio.sleep(0.2)
            else:
                await self._aio_stop()  # pytest.fail doesn't call stop_process
                raise Exception(
                    "Cannot start AioMotoService: {}".format(self._service_name)
                )

    async def _aio_stop(self):
        if self._server:
            self.reset()  # clear the service backends
            self._server.shutdown()

        self._thread.join()
