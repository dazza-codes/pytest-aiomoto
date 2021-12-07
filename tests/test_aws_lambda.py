from typing import Dict
from typing import List

import pytest

from pytest_aiomoto.aws_lambda import aws_lambda_src
from pytest_aiomoto.aws_lambda import aws_lambda_zip
from pytest_aiomoto.aws_lambda import lambda_handler


def test_lambda_handler_echo():
    event = {"i": 0}
    result = lambda_handler(event=event, context={})
    assert isinstance(result, Dict)
    assert result['statusCode'] == 200
    body = result['body']
    assert body == event


def test_lambda_handler_too_large():
    event = {"action": "too-large"}
    result = lambda_handler(event=event, context={})
    assert isinstance(result, Dict)
    assert result['statusCode'] == 200
    body = result['body']
    assert body
    assert isinstance(body, List)
    assert isinstance(body[0], str)
    assert body[0] == "xxx"
    assert len(body) == 1000000


def test_lambda_handler_raises():
    event = {"action": "runtime-error"}
    with pytest.raises(RuntimeError):
        lambda_handler(event=event, context={})


def test_aws_lambda_src():
    lambda_src = aws_lambda_src()
    assert isinstance(lambda_src, str)
    assert 'def lambda_handler' in lambda_src


def test_aws_lambda_zip():
    lambda_zip = aws_lambda_zip()
    assert isinstance(lambda_zip, bytes)
