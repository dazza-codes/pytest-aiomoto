# Copyright 2021 Darren Weber
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

from functools import partial

import pytest


@pytest.fixture()
def aio_s3fs(
    aio_aws_session,
    aio_aws_s3_server,
    mocker,
    monkeypatch,
):
    """
    The `aio_s3fs` fixture mocks generation of any `aiobotocore.client.S3` object
    so that it calls a localhost server provided by an asyncio version of the moto-server.
    The `aio_s3fs` fixture is simply a context to apply the mock, it is not intended to be a
    replacement for `s3fs`.  Just add the `aio_s3fs` fixture to a test function and then use
    `s3fs` as normal.
    """
    try:
        import s3fs

        try:
            monkeypatch.setenv("S3_ENDPOINT_URL", aio_aws_s3_server)
            aio_client_patch = mocker.patch(
                "aiobotocore.session.AioSession.create_client",
                side_effect=partial(
                    aio_aws_session.create_client, "s3", endpoint_url=aio_aws_s3_server
                )
            )
            s3fs.S3FileSystem.clear_instance_cache()

            yield

            assert aio_client_patch.call_count > 0

        finally:
            s3fs.S3FileSystem.clear_instance_cache()
            monkeypatch.delenv("S3_ENDPOINT_URL", raising=False)

    except ImportError:
        pytest.skip("The extra pytest_aiomoto[s3fs] dependency is missing")


# NOTE: S3FileSystem is very hard to patch completely; keeping these
#       attempts in this comment, although they did not work
# s3fs.S3FileSystem.clear_instance_cache()
# s3_file_system = s3fs.S3FileSystem(
#     anon=True,
#     client_kwargs={
#         "endpoint_url": s3_endpoint_url,
#         "region_name": aws_region
#     },
#     loop=event_loop,
#     asynchronous=True,
#     session=aio_aws_session
# )
# s3_file_system.invalidate_cache()
# s3_file_system._s3 = aio_aws_s3_client
# await s3_file_system.set_session()
# s3fs_patch = mocker.patch("s3fs.core.S3FileSystem")
# s3fs_patch.return_value = s3_file_system
