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


class S3Object(NamedTuple):
    """
    Just the bucket_name and key for an :code:`s3.ObjectSummary`.
    This simple named tuple should work around problems with :code:`Pickle`
    for an :code:`s3.ObjectSummary`
    """

    bucket: str
    key: str

    @property
    def bucket_name(self) -> str:
        return self.bucket

    @property
    def s3_uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"
