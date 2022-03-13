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
from typing import List

import boto3
import botocore.client
import pytest

from pytest_aiomoto.aws_clients import AwsEC2Client
from pytest_aiomoto.utils import AWS_REGION


def get_aws_region() -> str:
    return os.getenv("AWS_DEFAULT_REGION", AWS_REGION).strip()


class AwsRegions:
    def __init__(self, ec2_client: botocore.client.BaseClient = None):
        self._ec2_client = ec2_client
        self._response = None
        self._region_names = None
        self._default_region = None

    @property
    def ec2_client(self) -> AwsEC2Client:
        if self._ec2_client is None:
            self._ec2_client = boto3.client("ec2", region_name=self.default_region)
        return self._ec2_client

    @property
    def default_region(self):
        if self._default_region is None:
            self._default_region = get_aws_region()
        return self._default_region

    @property
    def region_names(self) -> List[str]:
        if self._region_names is None:
            if self._response is None:
                self._response = self.ec2_client.describe_regions()
            self._region_names = sorted(
                [r["RegionName"] for r in self._response["Regions"]]
            )
        return self._region_names


@pytest.fixture
def aws_regions(aws_ec2_client) -> List[str]:
    """
    All available AWS regions
    """
    aws_regions = AwsRegions(ec2_client=aws_ec2_client).region_names
    yield aws_regions


@pytest.fixture
def aws_region(monkeypatch) -> str:
    """
    A default AWS region - set as AWS_DEFAULT_REGION
    """
    monkeypatch.setenv("AWS_DEFAULT_REGION", AWS_REGION)
    yield AWS_REGION
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)


@pytest.fixture
def aws_region_us_west_2(monkeypatch) -> str:
    """
    The us-west-2 AWS region - set as AWS_DEFAULT_REGION
    """
    region = "us-west-2"
    monkeypatch.setenv("AWS_DEFAULT_REGION", region)
    yield region
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)


@pytest.fixture
def aws_region_us_east_1(monkeypatch) -> str:
    """
    The us-east-1 AWS region - set as AWS_DEFAULT_REGION
    """
    region = "us-east-1"
    monkeypatch.setenv("AWS_DEFAULT_REGION", region)
    yield region
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
