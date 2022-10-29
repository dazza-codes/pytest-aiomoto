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

import uuid

import pytest


@pytest.fixture
def aws_cognito_pool(cognito_moto_client, aws_region):
    name = str(uuid.uuid4())
    value = str(uuid.uuid4())
    response = cognito_moto_client.create_user_pool(
        PoolName=name, LambdaConfig={"PreSignUp": value}
    )
    yield response


@pytest.fixture
def aws_cognito_pool_client(cognito_moto_client, cognito_moto_pool):
    user_pool_id = cognito_moto_pool["UserPool"]["Id"]
    yield cognito_moto_client.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=str(uuid.uuid4())
    )
