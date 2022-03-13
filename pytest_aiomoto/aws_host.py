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

import os

import pytest

from pytest_aiomoto.utils import AWS_HOST
from pytest_aiomoto.utils import AWS_PORT


@pytest.fixture
def aws_host(monkeypatch):
    host = os.getenv("AWS_HOST", AWS_HOST)
    monkeypatch.setenv("AWS_HOST", host)
    yield
    monkeypatch.delenv("AWS_HOST", raising=False)


@pytest.fixture
def aws_port(monkeypatch):
    port = os.getenv("AWS_PORT", AWS_PORT)
    monkeypatch.setenv("AWS_PORT", port)
    yield
    monkeypatch.delenv("AWS_PORT", raising=False)


@pytest.fixture
def aws_proxy(aws_host, aws_port, monkeypatch):
    # only required if using a moto stand-alone server or similar local stack
    monkeypatch.setenv("HTTP_PROXY", f"http://{aws_host}:{aws_port}")
    monkeypatch.setenv("HTTPS_PROXY", f"http://{aws_host}:{aws_port}")
