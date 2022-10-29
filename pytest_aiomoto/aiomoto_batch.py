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
AWS test fixtures for AWS Batch

This test suite uses a large suite of moto mocks for the AWS batch
infrastructure. The infrastructure mocks are derived from the moto test
suite for testing the batch client. The test infrastructure should be used
according to the moto license. That license overrides any global license
applied to the pytest-aiomoto project.

.. seealso::

    - https://github.com/spulec/moto/pull/1197/files
    - https://github.com/spulec/moto/blob/master/tests/test_batch/test_batch.py
"""

from typing import NamedTuple
from typing import Optional

from aiobotocore.client import AioBaseClient

from pytest_aiomoto.utils import AWS_REGION


class AioBatchClient(AioBaseClient):
    pass


class AioEC2Client(AioBaseClient):
    pass


class AioECSClient(AioBaseClient):
    pass


class AioIAMClient(AioBaseClient):
    pass


class AioCloudWatchLogsClient(AioBaseClient):
    pass


class AioAwsBatchClients(NamedTuple):
    batch: AioBatchClient
    ec2: AioEC2Client
    ecs: AioECSClient
    iam: AioIAMClient
    logs: AioCloudWatchLogsClient
    region: str


class AioAwsBatchInfrastructure:
    aio_aws_clients: AioAwsBatchClients
    aws_region: str = AWS_REGION
    vpc_id: Optional[str] = None
    subnet_id: Optional[str] = None
    security_group_id: Optional[str] = None
    iam_arn: Optional[str] = None
    compute_env_name: Optional[str] = None
    compute_env_arn: Optional[str] = None
    job_queue_name: Optional[str] = None
    job_queue_arn: Optional[str] = None
    job_definition_name: Optional[str] = None
    job_definition_arn: Optional[str] = None


async def aio_batch_infrastructure(
    aio_aws_batch_clients: AioAwsBatchClients,
    aws_region: str,
    compute_env_name: str,
    job_queue_name: str,
    job_definition_name: str,
) -> AioAwsBatchInfrastructure:
    """
    Create AWS Batch infrastructure, including:
    - VPC with subnet
    - Security group and IAM role
    - Batch compute environment and job queue
    - Batch job job_definition

    This function is not a fixture so that tests can pass the AWS clients to it and then
    continue to use the infrastructure created by it while the client fixtures are in-tact for
    the duration of a test.
    """

    infrastructure = AioAwsBatchInfrastructure()
    infrastructure.aws_region = aws_region
    infrastructure.aio_aws_clients = aio_aws_batch_clients

    resp = await aio_aws_batch_clients.ec2.create_vpc(CidrBlock="172.30.0.0/24")
    vpc_id = resp["Vpc"]["VpcId"]

    resp = await aio_aws_batch_clients.ec2.create_subnet(
        AvailabilityZone=f"{aws_region}a", CidrBlock="172.30.0.0/25", VpcId=vpc_id
    )
    subnet_id = resp["Subnet"]["SubnetId"]

    resp = await aio_aws_batch_clients.ec2.create_security_group(
        Description="moto_test_sg_desc", GroupName="moto_test_sg", VpcId=vpc_id
    )
    sg_id = resp["GroupId"]

    resp = await aio_aws_batch_clients.iam.create_role(
        RoleName="MotoTestRole", AssumeRolePolicyDocument="moto_test_policy"
    )
    iam_arn = resp["Role"]["Arn"]

    resp = await aio_aws_batch_clients.batch.create_compute_environment(
        computeEnvironmentName=compute_env_name,
        type="UNMANAGED",
        state="ENABLED",
        serviceRole=iam_arn,
    )
    compute_env_arn = resp["computeEnvironmentArn"]

    resp = await aio_aws_batch_clients.batch.create_job_queue(
        jobQueueName=job_queue_name,
        state="ENABLED",
        priority=123,
        computeEnvironmentOrder=[{"order": 123, "computeEnvironment": compute_env_arn}],
    )
    assert resp["jobQueueName"] == job_queue_name
    assert resp["jobQueueArn"]
    job_queue_arn = resp["jobQueueArn"]

    resp = await aio_aws_batch_clients.batch.register_job_definition(
        jobDefinitionName=job_definition_name,
        type="container",
        containerProperties={
            "image": "alpine",
            "vcpus": 1,
            "memory": 8,
            "command": ["sleep", "2"],  # NOTE: job runs for 2 sec without overrides
        },
    )
    assert resp["jobDefinitionName"] == job_definition_name
    assert resp["jobDefinitionArn"]
    job_definition_arn = resp["jobDefinitionArn"]
    assert resp["revision"]
    assert resp["jobDefinitionArn"].endswith(
        "{0}:{1}".format(resp["jobDefinitionName"], resp["revision"])
    )

    infrastructure.vpc_id = vpc_id
    infrastructure.subnet_id = subnet_id
    infrastructure.security_group_id = sg_id
    infrastructure.iam_arn = iam_arn
    infrastructure.compute_env_name = compute_env_name
    infrastructure.compute_env_arn = compute_env_arn
    infrastructure.job_queue_name = job_queue_name
    infrastructure.job_queue_arn = job_queue_arn
    infrastructure.job_definition_name = job_definition_name
    infrastructure.job_definition_arn = job_definition_arn
    return infrastructure
