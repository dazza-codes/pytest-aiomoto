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


pytest_plugins = [
    "pytest_aiomoto.aws_regions",
    "pytest_aiomoto.aws_credentials",
    "pytest_aiomoto.aws_clients",
    "pytest_aiomoto.aws_batch",
    "pytest_aiomoto.aws_cognito",
    "pytest_aiomoto.aws_host",
    "pytest_aiomoto.aws_s3",
    "pytest_aiomoto.aiomoto_fixtures",
    "pytest_aiomoto.aiomoto_lambda",
    "pytest_aiomoto.aiomoto_s3",
    "pytest_aiomoto.aiomoto_s3fs",
]


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "aws_live: tests that require credentials for live AWS network requests"
    )
    config.addinivalue_line(
        "markers",
        "aws_s3: tests that require credentials for live AWS S3 network requests"
    )
