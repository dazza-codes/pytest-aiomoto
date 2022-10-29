
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

