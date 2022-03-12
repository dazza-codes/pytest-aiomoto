# Welcome to pytest-aiomoto

version: 0.3.1

[pytest](https://docs.pytest.org) fixtures for AWS services,
with support for asyncio fixtures using [aiobotocore](https://aiobotocore.readthedocs.io)

## Warning

- This package is work in progress, it is not recommended for production purposes.
  During the initial phases of this project, it is likely that some releases
  could introduce breaking changes in test fixtures.  It's highly
  recommended pinning this dependency to patch releases during the
  0.x.y releases.
- This package could restrict available versions of aws libs, including:
  aiobotocore, botocore, boto3, and moto.  The initial intention is to allow
  any 2.x.y versions of aiobotocore and moto.
- The fixtures in this package might not be optimized for concurrent testing.
  It is not known yet whether the fixtures are thread safe or adequately
  randomized to support parallel test suites.

## Installation

You can install "pytest-aiomoto" via pip

    $ pip install pytest-aiomoto

## Usage

To list the available fixtures

    $ pytest --fixtures

This project attempts to provide some common fixtures for commonly used
services.  As such, it is not a generic package for any services; the
moto project provides that and this project builds on that.  This
project aims to create some useful fixtures that behave nearly the
same way for both synchronous clients (botocore) and
asynchronous clients (aiobotocore).
