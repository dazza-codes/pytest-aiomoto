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

from typing import Optional

import pytest

from pytest_aiomoto.aws_clients import AwsBatchClients


@pytest.fixture
def aws_batch_clients(
    aws_batch_client,
    aws_ec2_client,
    aws_ecs_client,
    aws_iam_client,
    aws_logs_client,
    aws_region,
):
    return AwsBatchClients(
        batch=aws_batch_client,
        ec2=aws_ec2_client,
        ecs=aws_ecs_client,
        iam=aws_iam_client,
        logs=aws_logs_client,
        region=aws_region,
    )


@pytest.fixture(scope="session")
def job_queue_name():
    return "moto_test_job_queue"


@pytest.fixture(scope="session")
def job_definition_name():
    return "moto_test_job_definition"


@pytest.fixture(scope="session")
def compute_env_name():
    return "moto_test_compute_env"


class AwsBatchInfrastructure:
    aws_region: str
    aws_clients: AwsBatchClients
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


def batch_infrastructure(
    aws_clients: AwsBatchClients,
    compute_env_name: str,
    job_queue_name: str,
    job_definition_name: str,
) -> AwsBatchInfrastructure:
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

    infrastructure = AwsBatchInfrastructure()
    infrastructure.aws_region = aws_clients.region
    infrastructure.aws_clients = aws_clients

    resp = aws_clients.ec2.create_vpc(CidrBlock="172.30.0.0/24")
    vpc_id = resp["Vpc"]["VpcId"]

    resp = aws_clients.ec2.create_subnet(
        AvailabilityZone=f"{aws_clients.region}a",
        CidrBlock="172.30.0.0/25",
        VpcId=vpc_id,
    )
    subnet_id = resp["Subnet"]["SubnetId"]

    resp = aws_clients.ec2.create_security_group(
        Description="moto_test_sg_desc", GroupName="moto_test_sg", VpcId=vpc_id
    )
    sg_id = resp["GroupId"]

    resp = aws_clients.iam.create_role(
        RoleName="MotoTestRole", AssumeRolePolicyDocument="moto_test_policy"
    )
    iam_arn = resp["Role"]["Arn"]

    resp = aws_clients.batch.create_compute_environment(
        computeEnvironmentName=compute_env_name,
        type="UNMANAGED",
        state="ENABLED",
        serviceRole=iam_arn,
    )
    compute_env_arn = resp["computeEnvironmentArn"]

    resp = aws_clients.batch.create_job_queue(
        jobQueueName=job_queue_name,
        state="ENABLED",
        priority=123,
        computeEnvironmentOrder=[{"order": 123, "computeEnvironment": compute_env_arn}],
    )
    assert resp["jobQueueName"] == job_queue_name
    assert resp["jobQueueArn"]
    job_queue_arn = resp["jobQueueArn"]

    resp = aws_clients.batch.register_job_definition(
        jobDefinitionName=job_definition_name,
        type="container",
        containerProperties={
            "image": "busybox",
            "vcpus": 2,
            "memory": 8,
            "command": ["sleep", "10"],  # NOTE: job runs for 10 sec without overrides
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
