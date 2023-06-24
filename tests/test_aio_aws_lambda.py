# Copyright 2019-2023 Darren Weber
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

"""
Test Asyncio AWS Lambda

"""
import json
from typing import Dict

import pytest

from pytest_aiomoto.utils import response_success


@pytest.mark.asyncio
async def test_async_lambda_invoke_success(aws_lambda_func, aio_aws_lambda_client):

    event = {"i": 0}
    payload = json.dumps(event).encode()
    params = {
        "FunctionName": aws_lambda_func,
        "InvocationType": "RequestResponse",
        "LogType": "None",
        "Payload": payload
    }

    response = await aio_aws_lambda_client.invoke(**params)

    assert response.get("StatusCode") == 200
    assert response_success(response)

    metadata = response.get("ResponseMetadata")
    headers = metadata.get("HTTPHeaders")

    content_type = headers.get("content-type")
    assert content_type == "application/json"

    content_length = int(headers.get("content-length"))
    assert content_length > 0

    response_payload = response.get("Payload")
    if response_payload:
        async with response_payload as stream:
            data = await stream.read()

    # since this function should work, test the response data
    data = data.decode()
    body = json.loads(data)
    assert body == {"statusCode": 200, "body": event}


@pytest.mark.skip("https://github.com/spulec/moto/issues/3988")
@pytest.mark.asyncio
async def test_async_lambda_invoke_too_large(aws_lambda_func, aio_aws_lambda_client):
    # TODO: see also stub issue at https://github.com/aio-libs/aiobotocore/issues/781

    event = {"action": "too-large"}
    payload = json.dumps(event).encode()
    params = {
        "FunctionName": aws_lambda_func,
        "InvocationType": "RequestResponse",
        "LogType": "None",
        "Payload": payload
    }

    response = await aio_aws_lambda_client.invoke(**params)

    # Note that Lambda still has a 200 response code for errors
    assert response.get("StatusCode") == 200
    assert response_success(response)

    metadata = response.get("ResponseMetadata")
    headers = metadata.get("HTTPHeaders")

    content_length = int(headers.get("content-length"))
    assert content_length > 0

    response_payload = response.get("Payload")
    if response_payload:
        async with response_payload as stream:
            data = await stream.read()

    # lambda function error
    lambda_error = {
        "errorMessage": "Response payload size exceeded maximum allowed payload size (6291556 bytes).",
        "errorType": "Function.ResponseSizeTooLarge",
    }
    # assert response.get("FunctionError")
    error = data.decode()
    error = json.loads(error)
    assert isinstance(error, Dict)
    assert error.get("errorType") == lambda_error.get("errorType")
    assert error.get("errorMessage") == lambda_error.get("errorMessage")
    assert error.get("stackTrace")


@pytest.mark.asyncio
async def test_async_lambda_invoke_error(aws_lambda_func, aio_aws_lambda_client):

    event = {"action": "runtime-error"}
    payload = json.dumps(event).encode()
    params = {
        "FunctionName": aws_lambda_func,
        "InvocationType": "RequestResponse",
        "LogType": "None",
        "Payload": payload
    }

    response = await aio_aws_lambda_client.invoke(**params)

    # Note that Lambda still has a 200 response code for errors
    assert response.get("StatusCode") == 200
    assert response_success(response)

    metadata = response.get("ResponseMetadata")
    headers = metadata.get("HTTPHeaders")

    content_length = int(headers.get("content-length"))
    assert content_length > 0

    response_payload = response.get("Payload")
    if response_payload:
        async with response_payload as stream:
            data = await stream.read()

    # lambda function error
    assert response.get("FunctionError")
    error = data.decode()
    error = json.loads(error)
    assert isinstance(error, Dict)
    assert error.get("errorType") == "RuntimeError"
    assert error.get("errorMessage") == "runtime-error"
    assert error.get("stackTrace")
