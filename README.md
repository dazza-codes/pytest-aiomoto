# pytest-aiomoto

[![Build Status](https://github.com/dazza-codes/pytest-aiomoto/actions/workflows/python-test.yml/badge.svg)](https://github.com/dazza-codes/pytest-aiomoto/actions/workflows/python-test.yml)
[![Documentation Status](https://readthedocs.org/projects/pytest-aiomoto/badge/?version=latest)](https://pytest-aiomoto.readthedocs.io/en/latest/?badge=latest)

[![PyPI version](https://img.shields.io/pypi/v/pytest-aiomoto.svg)](https://pypi.org/project/pytest-aiomoto)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-aiomoto.svg)](https://pypi.org/project/pytest-aiomoto)

[pytest](https://docs.pytest.org) fixtures for AWS services,
with support for asyncio fixtures using
[aiobotocore](https://aiobotocore.readthedocs.io)

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

## Contributing

Contributions are welcome, if you build similar common fixtures or build
on the existing package fixtures.  The details for bug fixes could be
complicated, due to the dependencies on aiobotocore and moto.

Please review [github collaboration](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
practices.  Once you clone your fork of the repository:

    cd pytest-aiomoto
    make init
    make test

It's recommended that development use python 3.7, to avoid introducing any python
code that might not be compatible with the minimum version of python supported.  This
is important in the context of the general evolution of asyncio in python.

Most development is done in a linux context (e.g. Ubuntu LTS).  If some development
tools or common practices are not working as expected on OSX or Windows, there is
limited support for adapting to various development environments.

Tests are run with [pytest](https://github.com/pytest-dev/pytest), please ensure
the percentage of coverage at least stays the same before you submit a pull request.
The expectation for contributions might be a slow process, please do not anticipate
any turn around on the order of days (unless you're already a core contributor).
Using your own fork can be a faster way to evolve your fixtures for your use cases.

## Issues

If you encounter any problems, please
[file an issue](https://github.com/dazza-codes/pytest-aiomoto/issues)
along with a detailed description.

# License

Distributed under the terms of the
[Apache Software License 2.0](http://www.apache.org/licenses/LICENSE-2.0),
"pytest-aiomoto" is free and open source software.

```text
Copyright 2021 Darren Weber

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

# Notices

Inspiration for this project comes from testing the
[aio-aws](https://github.com/dazza-codes/aio-aws) project,
which uses the Apache 2 license.
