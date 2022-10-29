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

"""
Test Asyncio AWS Lambda

"""

import botocore.client
import botocore.exceptions
import pytest

from pytest_aiomoto.aws_lambda import aws_lambda_src
from pytest_aiomoto.aws_lambda import zip_lambda
from pytest_aiomoto.utils import response_success


@pytest.fixture
def aws_lambda_zip() -> bytes:
    return zip_lambda(aws_lambda_src())


@pytest.fixture
async def lambda_iam_role(aio_aws_iam_client):
    try:
        response = await aio_aws_iam_client.get_role(RoleName="my-role")
        return response["Role"]["Arn"]
    except botocore.client.ClientError:
        response = await aio_aws_iam_client.create_role(
            RoleName="my-role",
            AssumeRolePolicyDocument="some policy",
            Path="/my-path/",
        )
        return response["Role"]["Arn"]


@pytest.fixture
async def aws_lambda_func(
    aws_lambda_zip, lambda_iam_role, aio_aws_lambda_client
) -> str:

    func = "lambda_dev"

    response = await aio_aws_lambda_client.create_function(
        FunctionName=func,
        Runtime="python3.7",
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": aws_lambda_zip},
        Role=lambda_iam_role,
        Description="lambda_dev function",
        Timeout=10,
        MemorySize=128,
        Publish=True,
    )
    assert response_success(response)

    return func
