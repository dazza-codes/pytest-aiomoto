# Copyright 2019-2021 Darren Weber
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
import socket
from typing import Dict

from moto.core.models import BotocoreStubber

AWS_HOST = "127.0.0.1"
AWS_PORT = "5000"

AWS_REGION = "us-west-2"
AWS_ACCESS_KEY_ID = "test_AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "test_AWS_SECRET_ACCESS_KEY"


def assert_status_code(response, status_code: int):
    assert (
        int(response.get("ResponseMetadata", {}).get("HTTPStatusCode")) == status_code
    )


def get_free_tcp_port(release_socket: bool = False):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.bind(("", 0))
    addr, port = sckt.getsockname()
    if release_socket:
        sckt.close()
        return port

    return sckt, port


def has_moto_mocks(client, event_name):
    # moto registers mock callbacks with the `before-send` event-name, using
    # specific callbacks for the methods that are generated dynamically. By
    # checking that the first callback is a BotocoreStubber, this verifies
    # that moto mocks are intercepting client requests.
    callbacks = client.meta.events._emitter._lookup_cache[event_name]
    if len(callbacks) > 0:
        stub = callbacks[0]
        assert isinstance(stub, BotocoreStubber)
        return stub.enabled
    return False


def response_success(response: Dict) -> bool:
    """
    Parse a response from a request issued by any botocore.client.BaseClient
    to determine whether the request was successful or not.
    :param response:
    :return: boolean
    :raises: KeyError if the response is not an AWS response
    """
    # If the response dict is not constructed as expected for an AWS response,
    # this should raise a KeyError to indicate something is very wrong.
    status_code = int(response["ResponseMetadata"]["HTTPStatusCode"])
    if status_code:
        # consider 300+ responses to be unsuccessful
        return 200 <= status_code < 300
    else:
        return False
