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

import os

import boto3.session
import botocore.credentials
import botocore.session

from pytest_aiomoto.utils import AWS_ACCESS_KEY_ID
from pytest_aiomoto.utils import AWS_SECRET_ACCESS_KEY


def test_aws_credentials(aws_credentials):
    assert os.getenv("AWS_ACCESS_KEY_ID")
    assert os.getenv("AWS_SECRET_ACCESS_KEY")
    assert os.getenv("AWS_ACCESS_KEY_ID") == AWS_ACCESS_KEY_ID
    assert os.getenv("AWS_SECRET_ACCESS_KEY") == AWS_SECRET_ACCESS_KEY


def test_aws_default_credentials(default_profile, mock_default_session):
    assert os.getenv("AWS_DEFAULT_PROFILE") == "default"
    session = botocore.session.Session()
    profile = session.full_config.get("profiles").get("default")
    assert profile == default_profile


def test_mock_default_session(default_profile, mock_default_session):
    m_session = mock_default_session
    assert isinstance(m_session, boto3.session.Session)
    assert 'default' in m_session.available_profiles
    assert m_session.profile_name == 'default'
    m_credentials = m_session.get_credentials()
    assert isinstance(m_credentials, botocore.credentials.Credentials)
    assert m_credentials.access_key == default_profile["aws_access_key_id"]
    assert m_credentials.secret_key == default_profile["aws_secret_access_key"]
    assert os.getenv("AWS_DEFAULT_PROFILE") == "default"
    session = botocore.session.Session()
    profile = session.full_config.get("profiles").get("default")
    assert profile == default_profile


def test_mock_aws_credentials(default_profile, mock_default_credentials_file, aws_profile_credentials, monkeypatch):
    profile_name = "default"
    aws_region = default_profile["region"]

    profile_path = mock_default_credentials_file
    assert profile_path.exists()
    profile_file = str(profile_path.absolute())

    with aws_profile_credentials(
        profile_name=profile_name,
        aws_region=aws_region,
        profile_file=profile_file
    ) as m_session:
        assert isinstance(m_session, boto3.session.Session)
        assert 'default' in m_session.available_profiles
        assert m_session.profile_name == 'default'
        m_credentials = m_session.get_credentials()
        assert isinstance(m_credentials, botocore.credentials.Credentials)
        assert m_credentials.access_key == default_profile["aws_access_key_id"]
        assert m_credentials.secret_key == default_profile["aws_secret_access_key"]
        assert os.getenv("AWS_DEFAULT_PROFILE") == "default"
        session = botocore.session.Session()
        profile = session.full_config.get("profiles").get("default")
        assert profile == default_profile


def test_aws_credentials_missing_profile(aws_profile_credentials):
    with aws_profile_credentials(profile_name="missing-profile", aws_region="us-east-1"):
        # this test never gets here, it is skipped due to missing credentials
        assert False
