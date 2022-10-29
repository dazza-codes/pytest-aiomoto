"""
Configure the invoke release task
"""

from invoke_release.plugins import PatternReplaceVersionInFilesPlugin
from invoke_release.tasks import *  # noqa: F403


configure_release_parameters(  # noqa: F405
    module_name="pytest_aiomoto",
    display_name="pytest-aiomoto",
    # python_directory="package",
    plugins=[
        PatternReplaceVersionInFilesPlugin(
            "docs/index.md", "pytest_aiomoto/version.py", "pyproject.toml", "README.md"
        )
    ],
)
