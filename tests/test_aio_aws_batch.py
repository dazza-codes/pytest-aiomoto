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
Test Asyncio AWS Batch

This test suite uses a large suite of moto mocks for the AWS batch
infrastructure. These infrastructure mocks are derived from the moto test
suite for testing the batch client. The test infrastructure should be used
according to the moto license (Apache-2.0).

.. seealso::

    - https://github.com/spulec/moto/pull/1197/files
    - https://github.com/spulec/moto/blob/master/tests/test_batch/test_batch.py
"""

import pytest

from pytest_aiomoto.aiomoto_fixtures import AioAwsBatchClients
from pytest_aiomoto.aiomoto_fixtures import AioAwsBatchInfrastructure
from pytest_aiomoto.aiomoto_fixtures import aio_batch_infrastructure
from pytest_aiomoto.aws_batch_models import AWSBatchJobStates
from pytest_aiomoto.utils import response_success


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


@pytest.mark.asyncio
async def test_aws_batch_infrastructure(
    aio_aws_batch_infrastructure: AioAwsBatchInfrastructure,
):
    infrastructure = aio_aws_batch_infrastructure
    assert infrastructure
    assert infrastructure.vpc_id
    assert infrastructure.subnet_id
    assert infrastructure.security_group_id
    assert infrastructure.iam_arn
    assert infrastructure.compute_env_name
    assert infrastructure.compute_env_arn
    assert infrastructure.job_queue_name
    assert infrastructure.job_queue_arn
    assert infrastructure.job_definition_name
    assert infrastructure.job_definition_arn


@pytest.mark.asyncio
async def test_aio_batch_job_definitions(
    aio_aws_batch_infrastructure: AioAwsBatchInfrastructure,
):
    aws_resources = aio_aws_batch_infrastructure
    aws_region = aws_resources.aws_region
    job_definition_name = aws_resources.job_definition_name

    assert aws_resources
    assert aws_resources.job_definition_arn
    assert f"arn:aws:batch:{aws_region}" in aws_resources.job_definition_arn
    assert job_definition_name in aws_resources.job_definition_arn

    clients = aio_aws_batch_infrastructure.aio_aws_clients
    response = await clients.batch.describe_job_definitions()
    assert response_success(response)
    job_definitions = response["jobDefinitions"]
    assert len(job_definitions) == 1
    job_definition = job_definitions[0]
    assert job_definition["jobDefinitionArn"] == aws_resources.job_definition_arn
    assert job_definition["jobDefinitionName"] == aws_resources.job_definition_name


@pytest.mark.asyncio
async def test_aio_batch_job_queues(
    aio_aws_batch_infrastructure: AioAwsBatchInfrastructure,
):
    aws_resources = aio_aws_batch_infrastructure
    aws_region = aws_resources.aws_region
    job_queue_name = aws_resources.job_queue_name

    assert aws_resources
    assert aws_resources.job_queue_arn
    assert f"arn:aws:batch:{aws_region}" in aws_resources.job_queue_arn
    assert job_queue_name in aws_resources.job_queue_arn

    clients = aio_aws_batch_infrastructure.aio_aws_clients
    response = await clients.batch.describe_job_queues()
    assert response_success(response)
    job_queues = response["jobQueues"]
    assert len(job_queues) == 1
    job_queue = job_queues[0]
    assert job_queue["jobQueueArn"] == aws_resources.job_queue_arn
    assert job_queue["jobQueueName"] == aws_resources.job_queue_name


@pytest.mark.asyncio
async def test_aio_batch_list_jobs(
    aio_aws_batch_infrastructure: AioAwsBatchInfrastructure,
):
    clients = aio_aws_batch_infrastructure.aio_aws_clients
    job_queue_name = aio_aws_batch_infrastructure.job_queue_name
    
    job_states = [state.name for state in AWSBatchJobStates]

    for job_status in job_states:
        response = await clients.batch.list_jobs(
            jobQueue=job_queue_name, jobStatus=job_status
        )
        assert response_success(response)
        assert response["jobSummaryList"] == []
