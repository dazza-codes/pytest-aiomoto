
pytest_plugins = [
    "pytest_aiomoto.aws_fixtures",
    "pytest_aiomoto.aiomoto_fixtures",
    "pytest_aiomoto.aiomoto_lambda",
    "pytest_aiomoto.aiomoto_s3",
    "pytest_aiomoto.aiomoto_s3fs",
]


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "aws_live: tests that require credentials for live AWS network requests"
    )
    config.addinivalue_line(
        "markers",
        "aws_s3: tests that require credentials for live AWS S3 network requests"
    )
