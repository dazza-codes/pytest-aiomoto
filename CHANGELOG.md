
0.1.1 (2021-12-06)
------------------
Initial implementation for pytest-aiomoto fixtures


0.1.2 (2021-12-06)
------------------
- Cleanup package and enhance docs
- Move mkdocs to optional dependencies
- Add readthedocs config and requirements
- Update README


0.2.0 (2021-12-10)
------------------
- Add mocked aio_s3fs fixture, skips if s3fs is not installed
- Make s3fs an optional extra dependency
- Add tests for s3fs with aiobotocore moto-mocks
- Cleanup aws s3 test fixtures
- Use a UUID for any moto bucket name
- Add dev libs to test s3fs/pandas/xarray/zarr


0.3.0 (2022-02-23)
------------------
- Update moto 3.x
- Extract aiomoto utils for AWS Batch


0.3.1 (2022-03-12)
------------------
- Fix reset for moto.service backends
- Relax dependencies


0.4.0 (2022-03-12)
------------------
- Refactor AioMotoService
- Refactor moto fixtures into separate modules
- Add mock fixtures for AWS credentials
- Enhance aws fixtures
- Add python 3.8 to github test matrix
- Revise make test command details
- Add pytest.ini markers
- Relax dependency versions


0.5.0 (2022-07-09)
------------------
- Bump release to 0.5.0
- Bump release to 0.5.0-alpha.0
- Update Apache copyright dates in test files
- Update tests for AWS Batch infrastructure
- Use a UUID fixture for unique s3 artifacts
- Apply pytest-asyncio strict decorators on fixtures
- Use pytest-asyncio strict mode
- poetry update
- Update dependencies for pytest 7.x
- Return service objects from aio server fixtures
- Update documentation
- Revise make docs success/failure status
- poetry update
- Update mkdocs libs
- Isolate AWS Batch mock infrastructure and cleanup resources
- Ignore some warnings from distutils
- poetry update
- Relax some dependency versions


0.6.0 (2022-10-28)
------------------
- drop python 3.7 support
- update pytest-asyncio 0.20
- update aiofiles 22.x
- update moto 4.x


0.6.1 (2022-10-28)
------------------
- Bump python 3.7 to 3.8 - various
- Update readthedocs python version


0.6.2 (2022-11-08)
------------------
- Revise aggressive cleanup for AWS credentials
- Fix file permissions on pytest_aiomoto/aws_batch_models.py


0.6.3 (2022-11-08)
------------------
- Update poetry build system and dev-deps


0.7.0 (2023-06-24)
------------------
4d7e074 - Bump version 0.7.0 <Darren Weber>
e8ba493 - Remove invoke-release tasks <Darren Weber>
c5ac092 - Use versionner to manage releases <Darren Weber>
80a5ab9 - Update copyright dates <Darren Weber>
4c2e059 - Update make init recipe <Darren Weber>
e378446 - poetry update <Darren Weber>
41e0993 - Update libs; require s3fs with all extras for compatible AWS SDK libs <Darren Weber>
38b2ba0 - Revise github workflow, add python 3.11 <Darren Weber>


