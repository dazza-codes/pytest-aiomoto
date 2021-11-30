# -*- coding: utf-8 -*-

import pytest

# TODO: remove or adapt this module

def pytest_addoption(parser):
    group = parser.getgroup('aiomoto')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2021',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
