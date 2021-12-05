# pytest-aiomoto

[![Build Status](https://travis-ci.com/dazza-codes/pytest-aiomoto.svg?branch=main)](https://travis-ci.com/dazza-codes/pytest-aiomoto)
[![Documentation Status](https://readthedocs.org/projects/pytest-aiomoto/badge/?version=latest)](https://pytest-aiomoto.readthedocs.io/en/latest/?badge=latest)

[![PyPI version](https://img.shields.io/pypi/v/pytest-aiomoto.svg)](https://pypi.org/project/pytest-aiomoto)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-aiomoto.svg)](https://pypi.org/project/pytest-aiomoto)

[pytest](https://docs.pytest.org) fixtures for AWS services,
with support for asyncio fixtures using [aiobotocore](https://aiobotocore.readthedocs.io)

## Installation

You can install "pytest-aiomoto" via pip

    $ pip install pytest-aiomoto

## Usage

To list the available fixtures

    $ pytest --fixtures

## Contributing

Contributions are very welcome. Tests can be run with
[pytest](https://github.com/pytest-dev/pytest), please ensure
the coverage at least stays the same before you submit a pull request.

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
