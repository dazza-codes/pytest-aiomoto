# Copyright 2019-2021 Darren Weber
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

"""
AWS Lambda Utilities for Testing

"""
import inspect
import io
import zipfile


def lambda_handler(event, context):
    """
    A lambda handler for test purposes.
    This function must be self-contained, including imports required.
    """
    import sys

    print("event: %s" % event)
    action = event.get("action")
    if action == "too-large":
        x = ["xxx" for x in range(10 ** 6)]
        assert sys.getsizeof(x) > 6291556
        return {"statusCode": 200, "body": x}
    if action == "runtime-error":
        raise RuntimeError(action)
    return {"statusCode": 200, "body": event}


def aws_lambda_src() -> str:
    return inspect.getsource(lambda_handler)


def aws_lambda_zip() -> bytes:
    return zip_lambda(aws_lambda_src())


def zip_lambda(func_str) -> bytes:
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED)
    zip_file.writestr("lambda_function.py", func_str)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()
