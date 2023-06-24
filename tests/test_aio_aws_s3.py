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

import aiobotocore
import aiobotocore.client
import aiobotocore.config
import botocore.exceptions
import pytest
from aiobotocore.session import get_session

from pytest_aiomoto.utils import response_success


@pytest.mark.asyncio
async def test_aio_s3_list_bucket(aio_aws_s3_client, aio_s3_bucket):
    resp = await aio_aws_s3_client.list_buckets()
    assert response_success(resp)
    bucket_names = [b["Name"] for b in resp["Buckets"]]
    assert bucket_names == [aio_s3_bucket]


@pytest.mark.asyncio
async def test_aio_s3_list_buckets(aio_aws_s3_client, aio_s3_buckets):
    resp = await aio_aws_s3_client.list_buckets()
    assert response_success(resp)
    bucket_names = [b["Name"] for b in resp["Buckets"]]
    assert bucket_names == aio_s3_buckets


@pytest.mark.asyncio
async def test_aio_s3_object_head(
    aio_s3_bucket_name, aio_s3_key, aio_s3_bucket, aio_s3_object_text, aio_aws_s3_client
):
    resp = await aio_aws_s3_client.put_object(
        Bucket=aio_s3_bucket_name,
        Key=aio_s3_key,
        Body=aio_s3_object_text,
        ACL="public-read-write",
    )
    assert response_success(resp)
    resp = await aio_aws_s3_client.head_object(Bucket=aio_s3_bucket_name, Key=aio_s3_key)
    assert response_success(resp)


@pytest.mark.asyncio
async def test_aio_s3_bucket_head_not_authorized():

    session = get_session()
    aio_config = aiobotocore.config.AioConfig(max_pool_connections=1)
    session.set_default_client_config(aio_config)
    session.set_credentials("fake_AWS_ACCESS_KEY_ID", "fake_AWS_SECRET_ACCESS_KEY")

    async with session.create_client("s3") as client:
        with pytest.raises(botocore.exceptions.ClientError) as err:
            await client.head_bucket(Bucket="missing-bucket")

    msg = err.value.args[0]
    assert "HeadBucket operation" in msg
    assert "403" in msg
    assert "Forbidden" in msg


@pytest.mark.skip("https://github.com/aio-libs/aiobotocore/issues/781")
@pytest.mark.asyncio
async def test_aio_s3_bucket_head_too_many_requests():

    session = get_session()
    aio_config = aiobotocore.config.AioConfig(max_pool_connections=1)
    session.set_default_client_config(aio_config)
    session.set_credentials("fake_AWS_ACCESS_KEY_ID", "fake_AWS_SECRET_ACCESS_KEY")

    async with session.create_client("s3") as client:

        # TODO: HOW TO ADD HTTP STUBBER HERE, similar to:
        #   https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html

        with pytest.raises(botocore.exceptions.ClientError) as err:
            await client.head_bucket(Bucket="missing-bucket")

    msg = err.value.args[0]
    assert "HeadBucket operation" in msg
    assert "403" in msg
    assert "Forbidden" in msg
