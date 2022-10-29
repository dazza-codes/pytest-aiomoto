from functools import partial

import pytest

# NOTE: S3FileSystem is very hard to patch completely; keeping these
#       attempts in this comment, although they did not work
# s3fs.S3FileSystem.clear_instance_cache()
# s3_file_system = s3fs.S3FileSystem(
#     anon=True,
#     client_kwargs={
#         "endpoint_url": s3_endpoint_url,
#         "region_name": aws_region
#     },
#     loop=event_loop,
#     asynchronous=True,
#     session=aio_aws_session
# )
# s3_file_system.invalidate_cache()
# s3_file_system._s3 = aio_aws_s3_client
# await s3_file_system.set_session()
# s3fs_patch = mocker.patch("s3fs.core.S3FileSystem")
# s3fs_patch.return_value = s3_file_system


@pytest.fixture()
def aio_s3fs(
    aio_aws_session,
    aio_aws_s3_server,
    mocker,
    monkeypatch,
):
    import s3fs

    try:
        monkeypatch.setenv("S3_ENDPOINT_URL", aio_aws_s3_server)
        mocker.patch(
            "aiobotocore.session.AioSession.create_client",
            new=partial(
                aio_aws_session.create_client, "s3", endpoint_url=aio_aws_s3_server
            )
        )
        s3fs.S3FileSystem.clear_instance_cache()

        yield

    finally:
        s3fs.S3FileSystem.clear_instance_cache()
        monkeypatch.delenv("S3_ENDPOINT_URL", raising=False)


@pytest.mark.asyncio
async def test_pandas_s3_io(
    aio_s3_bucket, aio_s3fs
):
    import numpy as np
    import pandas as pd

    s3_file = f"s3://{aio_s3_bucket}/data.csv"
    print(s3_file)
    data = {"1": np.random.rand(5)}
    df = pd.DataFrame(data=data)
    df.to_csv(s3_file)
    s3_df = pd.read_csv(s3_file, index_col=0)
    assert isinstance(s3_df, pd.DataFrame)
    pd.testing.assert_frame_equal(df, s3_df)


@pytest.mark.asyncio
async def test_zarr_s3_io(
    aio_s3_bucket, aio_s3fs
):
    import numpy as np
    import pandas as pd
    import s3fs
    import xarray as xr

    fmap = s3fs.S3Map(f"s3://{aio_s3_bucket}/test_datasets/test.zarr", s3=s3fs.S3FileSystem())
    print(fmap.root)
    ds = xr.Dataset(
        {"foo": (("x", "y"), np.random.rand(4, 5))},
        coords={
            "x": [10, 20, 30, 40],
            "y": pd.date_range("2000-01-01", periods=5),
            "z": ("x", list("abcd")),
        },
    )
    ds.to_zarr(fmap, consolidated=True)
    s3_ds = xr.open_zarr(fmap, consolidated=True)
    assert isinstance(s3_ds, xr.Dataset)
    xr.testing.assert_equal(ds, s3_ds)
