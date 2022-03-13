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

from contextlib import contextmanager
from copy import deepcopy
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
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


def get_default_profile() -> Dict:
    """
    a default profile key:value pairs
    """
    return deepcopy({
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region": AWS_REGION
    })


def get_default_profile_credentials_content():
    default_profile = get_default_profile()
    return f"""
[default]
aws_access_key_id = {default_profile["aws_access_key_id"]}
aws_secret_access_key = {default_profile["aws_secret_access_key"]}
region = {default_profile["region"]}
"""


def get_default_profile_config_content():
    default_profile = get_default_profile()
    return f"""
[profile default]
aws_access_key_id = {default_profile["aws_access_key_id"]}
aws_secret_access_key = {default_profile["aws_secret_access_key"]}
region = {default_profile["region"]}
output = json
"""


def clean_aws_credentials(monkeypatch):
    """
    This uses monkeypatch to clear awscli environment variables and applies:

        boto3.DEFAULT_SESSION = None
        S3FileSystem.clear_instance_cache()

    """
    # See https://github.com/dask/s3fs/issues/461 for details about
    # s3fs using an instance cache with stored credentials.
    boto3.DEFAULT_SESSION = None
    S3FileSystem.clear_instance_cache()
    monkeypatch.delenv("AWS_CONFIG_FILE", raising=False)
    monkeypatch.delenv("AWS_SHARED_CREDENTIALS_FILE", raising=False)
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_PROFILE", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("AWS_ACCOUNT", raising=False)
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    monkeypatch.delenv("AWS_SECURITY_TOKEN", raising=False)
    monkeypatch.delenv("AWS_SESSION_TOKEN", raising=False)


def setup_aws_credentials(profile_name, aws_region=None, profile_file=None, monkeypatch=None) -> boto3.session.Session:
    """
    Any clients created from this session will use credentials
    from the [profile_name] section of ~/.aws/credentials.

    This assumes the profile_name is available in user credentials,
    it does not mock the credentials.

    It yields a `boto3.Session` for the named profile, and it uses
    monkeypatch to set awscli environment variables with the profile credentials.
    """
    monkeypatch.setenv("AWS_DEFAULT_PROFILE", profile_name)
    monkeypatch.setenv("AWS_DEFAULT_REGION", aws_region)
    if profile_file:
        monkeypatch.setenv("AWS_CONFIG_FILE", profile_file)
        monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", profile_file)
    session = boto3.Session(profile_name=profile_name, region_name=aws_region)
    credentials = session.get_credentials().get_frozen_credentials()
    monkeypatch.setenv("AWS_PROFILE", session.profile_name)
    monkeypatch.setenv("AWS_DEFAULT_PROFILE", session.profile_name)
    monkeypatch.setenv("AWS_DEFAULT_REGION", session.region_name)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", credentials.access_key)
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", credentials.secret_key)
    return session


@contextmanager
def patch_aws_profile_credentials(profile_name, aws_region=None, profile_file=None, monkeypatch=None) -> boto3.session.Session:
    """
    This returns a context manager that applies awscli credentials for
    a named profile - it assumes the named profile is available - and it
    will use monkeypatch to set awscli environment variables with those
    credentials.  It cleans up the environment variables.
    """
    try:
        clean_aws_credentials(monkeypatch)
        session = setup_aws_credentials(
            profile_name,
            aws_region=aws_region,
            profile_file=profile_file,
            monkeypatch=monkeypatch,
        )
        yield session
        clean_aws_credentials(monkeypatch)

    except ProfileNotFound:
        # Skip for missing credentials
        clean_aws_credentials(monkeypatch)
        pytest.skip(f"Missing AWS credentials ({profile_name}), skipping test")

    finally:
        clean_aws_credentials(monkeypatch)


@contextmanager
def ctx_aws_default_credentials_file(monkeypatch) -> Path:
    """
    This returns a context manager that mocks [default] profile credentials
    in a temporary credentials file.

    ... seealso::
        - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file
        - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list

    """
    credentials_ini = get_default_profile_credentials_content()
    config_ini = get_default_profile_config_content()

    clean_aws_credentials(monkeypatch)
    with TemporaryDirectory(prefix="pytest_aiomoto_") as dirname:
        try:
            tmp_path = Path(dirname)

            credentials_path = tmp_path / ".aws" / "credentials"
            # credentials_path = Path(credentials_file)
            if not credentials_path.exists():
                credentials_path.parent.mkdir(parents=True, exist_ok=True)
                credentials_path.touch(exist_ok=True)
            credentials_path.write_text(credentials_ini)
            credentials_mock_data = credentials_path.read_text()
            assert credentials_mock_data == credentials_ini

            config_path = tmp_path / ".aws" / "config"
            if not config_path.exists():
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.touch(exist_ok=True)
            config_path.write_text(config_ini)
            config_mock_data = config_path.read_text()
            assert config_mock_data == config_ini

            # Note: boto3 seems to read the credentials file, not the config file;
            #       whereas the awscli might prefer the config file; and they use
            #       different env-vars for custom file locations.
            credentials_file = str(credentials_path.absolute())
            monkeypatch.setenv("AWS_CONFIG_FILE", credentials_file)
            monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE",  credentials_file)
            yield credentials_path
            clean_aws_credentials(monkeypatch)

        finally:
            clean_aws_credentials(monkeypatch)


@contextmanager
def ctx_aws_default_credentials(monkeypatch) -> boto3.session.Session:
    """
    This returns a context manager that applies awscli credentials for
    a named profile - it assumes the named profile is available - and it
    will use monkeypatch to set awscli environment variables with those
    credentials.  It cleans up the environment variables.
    """
    profile_name = "default"
    default_profile = get_default_profile()
    aws_region = default_profile["region"]

    with ctx_aws_default_credentials_file(monkeypatch) as profile_path:
        assert profile_path.exists()
        profile_file = str(profile_path.absolute())
        try:
            session = botocore.session.Session()
            profiles = session.full_config.get("profiles")
            profile = profiles.get("default")
            assert profile == default_profile

            session = setup_aws_credentials(
                profile_name,
                aws_region=aws_region,
                profile_file=profile_file,
                monkeypatch=monkeypatch,
            )
            yield session
            clean_aws_credentials(monkeypatch)

        except ProfileNotFound:
            # Skip for missing credentials
            clean_aws_credentials(monkeypatch)
            pytest.skip(f"Missing AWS credentials ({profile_name}), skipping test")

        finally:
            clean_aws_credentials(monkeypatch)


@pytest.fixture
def default_profile() -> Dict:
    """
    a default profile key:value pairs
    """
    return get_default_profile()


@pytest.fixture
def default_profile_credentials_content(default_profile) -> str:
    """
    A string for the [default] entry in ~/.aws/credentials file
    """
    return get_default_profile_credentials_content()


@pytest.fixture
def aws_profile_credentials(monkeypatch) -> Callable:
    """
    This returns a context manager that applies awscli credentials for
    a named profile - it assumes the named profile is available - and it
    will use monkeypatch to set awscli environment variables with those
    credentials.  It cleans up the environment variables.

    The context manager returned is used like so:

        with mock_aws_credentials(profile_name, aws_region) as profile_session:
            assert isinstance(profile_session, boto3.session.Session)

    """
    return partial(patch_aws_profile_credentials, monkeypatch=monkeypatch)


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
def mock_default_credentials_file(monkeypatch) -> Path:
    """
    A context manager to mock a default profile in a
    mocked temporary file like ~/.aws/credentials
    """
    with ctx_aws_default_credentials_file(monkeypatch) as profile_path:
        yield profile_path


@pytest.fixture
def mock_default_session(monkeypatch) -> boto3.session.Session:
    """
    A context manager to mock a session with a default profile by
    creating a mocked temporary file like ~/.aws/credentials
    """
    with ctx_aws_default_credentials(monkeypatch) as m_session:
        yield m_session


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
