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

from typing import NamedTuple

import boto3
import botocore.client
import pytest
from boto3.resources.base import ServiceResource
from moto import mock_batch
from moto import mock_cognitoidp
from moto import mock_ec2
from moto import mock_ecs
from moto import mock_iam
from moto import mock_lambda
from moto import mock_logs
from moto import mock_s3
from moto import mock_secretsmanager
from moto import mock_sqs

from pytest_aiomoto.moto_services import moto_service_reset


class AwsBatchClient(botocore.client.BaseClient):
    pass


class AwsCognitoClient(botocore.client.BaseClient):
    pass


class AwsEC2Client(botocore.client.BaseClient):
    pass


class AwsECSClient(botocore.client.BaseClient):
    pass


class AwsIAMClient(botocore.client.BaseClient):
    pass


class AwsLambdaClient(botocore.client.BaseClient):
    pass


class AwsLogsClient(botocore.client.BaseClient):
    pass


class AwsS3Client(botocore.client.BaseClient):
    pass


class AwsSecretsClient(botocore.client.BaseClient):
    pass


class AwsSqsClient(botocore.client.BaseClient):
    pass


class AwsS3Resource(ServiceResource):
    pass


class AwsSqsResource(ServiceResource):
    pass


class AwsBatchClients(NamedTuple):
    batch: AwsBatchClient
    ec2: AwsEC2Client
    ecs: AwsECSClient
    iam: AwsIAMClient
    logs: AwsLogsClient
    region: str


@pytest.fixture
def aws_batch_client(aws_region) -> AwsBatchClient:
    with mock_batch():
        yield boto3.client("batch", region_name=aws_region)
    moto_service_reset("batch")


@pytest.fixture
def aws_cognito_client(aws_region) -> AwsCognitoClient:
    with mock_cognitoidp():
        yield boto3.client("cognito-idp", region_name=aws_region)
    moto_service_reset("cognito-idp")


@pytest.fixture
def aws_ec2_client(aws_region) -> AwsEC2Client:
    with mock_ec2():
        yield boto3.client("ec2", region_name=aws_region)
    moto_service_reset("ec2")


@pytest.fixture
def aws_ecs_client(aws_region) -> AwsECSClient:
    with mock_ecs():
        yield boto3.client("ecs", region_name=aws_region)
    moto_service_reset("ecs")


@pytest.fixture
def aws_iam_client(aws_region) -> AwsIAMClient:
    with mock_iam():
        yield boto3.client("iam", region_name=aws_region)
    moto_service_reset("iam")


@pytest.fixture
def aws_lambda_client(aws_region) -> AwsLambdaClient:
    with mock_lambda():
        yield boto3.client("lambda", region_name=aws_region)
    moto_service_reset("lambda")


@pytest.fixture
def aws_logs_client(aws_region) -> AwsLogsClient:
    with mock_logs():
        yield boto3.client("logs", region_name=aws_region)
    moto_service_reset("logs")


@pytest.fixture
def aws_s3_client(aws_region) -> AwsS3Client:
    with mock_s3():
        yield boto3.client("s3", region_name=aws_region)
    moto_service_reset("s3")


@pytest.fixture
def aws_s3_resource(aws_region) -> AwsS3Resource:
    with mock_s3():
        yield boto3.resource("s3", region_name=aws_region)
    moto_service_reset("s3")


@pytest.fixture
def aws_secrets_client(aws_region) -> AwsSecretsClient:
    with mock_secretsmanager():
        yield boto3.client("secretsmanager", region_name=aws_region)
    moto_service_reset("secretsmanager")


@pytest.fixture
def aws_sqs_client(aws_region) -> AwsSqsClient:
    with mock_sqs():
        yield boto3.client("sqs", region_name=aws_region)
    moto_service_reset("sqs")


@pytest.fixture
def aws_sqs_resource(aws_region) -> AwsSqsResource:
    with mock_sqs():
        yield boto3.resource("sqs", region_name=aws_region)
    moto_service_reset("sqs")

