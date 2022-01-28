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
from contextlib import contextmanager
from functools import partial
from typing import Callable
from typing import Dict

import boto3
import boto3.session
import botocore.session
import pytest
from botocore.exceptions import ProfileNotFound
from s3fs import S3FileSystem

from pytest_aiomoto.utils import AWS_ACCESS_KEY_ID
from pytest_aiomoto.utils import AWS_REGION
from pytest_aiomoto.utils import AWS_SECRET_ACCESS_KEY


def clean_aws_credentials(monkeypatch):
    # See https://github.com/dask/s3fs/issues/461 for details about
    # s3fs using an instance cache with stored credentials.
    boto3.DEFAULT_SESSION = None
    S3FileSystem.clear_instance_cache()
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_PROFILE", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("AWS_ACCOUNT", raising=False)
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    monkeypatch.delenv("AWS_SECURITY_TOKEN", raising=False)
    monkeypatch.delenv("AWS_SESSION_TOKEN", raising=False)


def setup_aws_credentials(profile_name, aws_region, monkeypatch) -> boto3.session.Session:
    # Any clients created from this session will use credentials
    # from the [profile_name] section of ~/.aws/credentials.
    monkeypatch.setenv("AWS_DEFAULT_PROFILE", profile_name)
    monkeypatch.setenv("AWS_DEFAULT_REGION", aws_region)
    session = boto3.Session(profile_name=profile_name, region_name=aws_region)
    credentials = session.get_credentials().get_frozen_credentials()
    monkeypatch.setenv("AWS_PROFILE", session.profile_name)
    monkeypatch.setenv("AWS_DEFAULT_PROFILE", session.profile_name)
    monkeypatch.setenv("AWS_DEFAULT_REGION", session.region_name)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", credentials.access_key)
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", credentials.secret_key)
    return session


@contextmanager
def patch_aws_credentials(profile_name, aws_region, monkeypatch):
    try:
        clean_aws_credentials(monkeypatch)
        session = setup_aws_credentials(profile_name, aws_region, monkeypatch)
        yield session
        clean_aws_credentials(monkeypatch)

    except ProfileNotFound:
        # Skip for missing credentials
        clean_aws_credentials(monkeypatch)
        pytest.skip(f"Missing AWS credentials ({profile_name}), skipping test")

    finally:
        clean_aws_credentials(monkeypatch)


@pytest.fixture
def mock_aws_credentials(monkeypatch) -> Callable:
    """
    provide a context manager to activate a named AWS profile,
    with mocked env-vars that are specific to the context.
    """
    return partial(patch_aws_credentials, monkeypatch=monkeypatch)


@pytest.fixture
def default_profile(monkeypatch) -> Dict:
    """
    mock a default profile key:value pairs
    """
    return {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region": AWS_REGION
    }


@pytest.fixture
def default_profile_ini(default_profile) -> str:
    """
    A [default] entry block for a ~/.aws/credentials file
    """
    return f"""
    [default]
    aws_access_key_id = {default_profile["aws_access_key_id"]}
    aws_secret_access_key =  {default_profile["aws_secret_access_key"]}
    region = {default_profile["region"]}
    """


@pytest.fixture
def mock_default_profile(default_profile, mocker, monkeypatch) -> Dict:
    """
    mock a default profile by patching botocore.session.Session.get_scoped_config
    """
    mock_config = mocker.patch(
        "botocore.session.Session.get_scoped_config"
    )
    mock_config.return_value = default_profile
    yield default_profile


@pytest.fixture
def mock_default_credentials(default_profile, mocker, monkeypatch) -> Dict:
    """
    mock a default profile by patching a mocked file for ~/.aws/credentials
    """

    profile_name = "default"
    aws_region = default_profile["region"]
    try:
        clean_aws_credentials(monkeypatch)

        aws_credentials_file = mocker.mock_open(
            read_data=f"""
        [default]
        aws_access_key_id = {default_profile["aws_access_key_id"]}
        aws_secret_access_key =  {default_profile["aws_secret_access_key"]}
        region = {default_profile["region"]}
        """
        )
        m = mocker.patch("builtins.open", aws_credentials_file)
        session = botocore.session.Session()
        profile = session.full_config.get("profiles").get("default")
        assert profile == default_profile
        profile_file = os.getenv("HOME") + "/.aws/credentials"
        m.assert_called_with(profile_file, encoding=None)

        session = setup_aws_credentials(profile_name, aws_region, monkeypatch)
        yield session
        clean_aws_credentials(monkeypatch)

    except ProfileNotFound:
        # Skip for missing credentials
        clean_aws_credentials(monkeypatch)
        pytest.skip(f"Missing AWS credentials ({profile_name}), skipping test")

    finally:
        clean_aws_credentials(monkeypatch)


@pytest.fixture
def aws_credentials(aws_region, monkeypatch):
    """Mocked AWS Credentials for moto."""
    try:
        clean_aws_credentials(monkeypatch)

        monkeypatch.setenv("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
        monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
        monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")

        yield
        clean_aws_credentials(monkeypatch)

    finally:
        clean_aws_credentials(monkeypatch)
