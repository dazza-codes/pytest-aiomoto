# Copyright 2021 Darren Weber
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

# To see moto-server logs
# pytest -s -p no:logging tests/test_aio_s3fs.py

import pytest


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
