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
AWS test fixtures

This test suite uses a large suite of moto mocks for the AWS batch
infrastructure. These infrastructure mocks are derived from the moto test
suite for testing the batch client. The test infrastructure should be used
according to the moto license. That license overrides any global license
applied to my aio_aws project.

.. seealso::

    - https://github.com/spulec/moto/pull/1197/files
    - https://github.com/spulec/moto/blob/master/tests/test_batch/test_batch.py
"""

import pytest
from aiobotocore.config import AioConfig
from aiobotocore.session import get_session

from pytest_aiomoto.aiomoto_batch import AioAwsBatchClients
from pytest_aiomoto.aiomoto_batch import AioAwsBatchInfrastructure
from pytest_aiomoto.aiomoto_batch import aio_batch_infrastructure
from pytest_aiomoto.aiomoto_services import MotoService
from pytest_aiomoto.utils import AWS_ACCESS_KEY_ID
from pytest_aiomoto.utils import AWS_SECRET_ACCESS_KEY


@pytest.fixture
async def aio_aws_batch_server():
    async with MotoService("batch") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_cloudformation_server():
    async with MotoService("cloudformation") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_ec2_server():
    async with MotoService("ec2") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_ecs_server():
    async with MotoService("ecs") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_iam_server():
    async with MotoService("iam") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_dynamodb2_server():
    async with MotoService("dynamodb2") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_lambda_server():
    async with MotoService("lambda") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_logs_server():
    # cloud watch logs
    async with MotoService("logs") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_s3_server():
    async with MotoService("s3") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_sns_server():
    async with MotoService("sns") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
async def aio_aws_sqs_server():
    async with MotoService("sqs") as svc:
        svc.reset()
        yield svc.endpoint_url
        svc.reset()


@pytest.fixture
def aio_aws_session(aws_credentials, aws_region, event_loop):
    # pytest-asyncio provides and manages the `event_loop`
    # and it should be set as the default loop for this session
    assert event_loop  # but it's not == asyncio.get_event_loop() ?

    session = get_session()
    session.user_agent_name = "aiomoto"

    assert session.get_default_client_config() is None
    aioconfig = AioConfig(max_pool_connections=1, region_name=aws_region)

    # Note: tried to use proxies for the aiobotocore.endpoint, to replace
    #      'https://batch.us-west-2.amazonaws.com/v1/describejobqueues', but
    #      the moto.server does not behave as a proxy server.  Leaving this
    #      here for the record to avoid trying to do it again sometime later.
    # proxies = {
    #     'http': os.getenv("HTTP_PROXY", "http://127.0.0.1:5000/moto-api/"),
    #     'https': os.getenv("HTTPS_PROXY", "http://127.0.0.1:5000/moto-api/"),
    # }
    # assert aioconfig.proxies is None
    # aioconfig.proxies = proxies

    session.set_default_client_config(aioconfig)
    assert session.get_default_client_config() == aioconfig

    session.set_credentials(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    session.set_debug_logger(logger_name="aiomoto")

    yield session


@pytest.fixture
def aio_aws_client(aio_aws_session):
    async def _get_client(service_name):
        async with MotoService(service_name) as srv:
            async with aio_aws_session.create_client(
                service_name, endpoint_url=srv.endpoint_url
            ) as client:
                yield client

    return _get_client


@pytest.fixture
async def aio_aws_batch_client(aio_aws_session, aio_aws_batch_server):
    async with aio_aws_session.create_client(
        "batch", endpoint_url=aio_aws_batch_server
    ) as client:
        yield client


@pytest.fixture
async def aio_aws_ec2_client(aio_aws_session, aio_aws_ec2_server):
    async with aio_aws_session.create_client(
        "ec2", endpoint_url=aio_aws_ec2_server
    ) as client:
        yield client


@pytest.fixture
async def aio_aws_ecs_client(aio_aws_session, aio_aws_ecs_server):
    async with aio_aws_session.create_client(
        "ecs", endpoint_url=aio_aws_ecs_server
    ) as client:
        yield client


@pytest.fixture
async def aio_aws_iam_client(aio_aws_session, aio_aws_iam_server):
    async with aio_aws_session.create_client(
        "iam", endpoint_url=aio_aws_iam_server
    ) as client:
        client.meta.config.region_name = "aws-global"  # not AWS_REGION
        yield client


@pytest.fixture
async def aio_aws_lambda_client(aio_aws_session, aio_aws_lambda_server):
    async with aio_aws_session.create_client(
        "lambda", endpoint_url=aio_aws_lambda_server
    ) as client:
        yield client


@pytest.fixture
async def aio_aws_logs_client(aio_aws_session, aio_aws_logs_server):
    async with aio_aws_session.create_client(
        "logs", endpoint_url=aio_aws_logs_server
    ) as client:
        yield client


@pytest.fixture
async def aio_aws_s3_client(aio_aws_session, aio_aws_s3_server, mocker):
    async with aio_aws_session.create_client(
        "s3", endpoint_url=aio_aws_s3_server
    ) as client:
        # TODO: find a way to apply this method mock only for creating "s3" clients;
        # # ensure the session returns the mock s3 client
        # mocker.patch.object(
        #     aiobotocore.session.AioClientCreator, "create_client",
        #     return_value=client
        # )
        yield client


@pytest.fixture
async def aio_aws_batch_clients(
    aio_aws_batch_client,
    aio_aws_ec2_client,
    aio_aws_ecs_client,
    aio_aws_iam_client,
    aio_aws_logs_client,
    aws_region,
):
    return AioAwsBatchClients(
        batch=aio_aws_batch_client,
        ec2=aio_aws_ec2_client,
        ecs=aio_aws_ecs_client,
        iam=aio_aws_iam_client,
        logs=aio_aws_logs_client,
        region=aws_region,
    )


@pytest.fixture
async def aio_aws_batch_infrastructure(
        aio_aws_batch_clients: AioAwsBatchClients,
        compute_env_name: str,
        job_queue_name: str,
        job_definition_name: str,
) -> AioAwsBatchInfrastructure:
    aws_region = aio_aws_batch_clients.region
    aws_resources = await aio_batch_infrastructure(
        aio_aws_batch_clients,
        aws_region,
        compute_env_name,
        job_queue_name,
        job_definition_name,
    )
    return aws_resources
