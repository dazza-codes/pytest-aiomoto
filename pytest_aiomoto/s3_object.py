from typing import NamedTuple


class S3Object(NamedTuple):
    """
    Just the bucket_name and key for an :code:`s3.ObjectSummary`.
    This simple named tuple should work around problems with :code:`Pickle`
    for an :code:`s3.ObjectSummary`
    """

    bucket: str
    key: str

    @property
    def bucket_name(self) -> str:
        return self.bucket

    @property
    def s3_uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"
