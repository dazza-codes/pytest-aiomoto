# Copyright 2019-2021 Darren Weber
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

"""
AWS Batch Utilities
===================

"""

import enum
from dataclasses import dataclass
from functools import total_ordering
from typing import Dict
from typing import List
from typing import Union


def gb_to_mib(gb: Union[int, float]) -> float:
    """
    Gigabyte (Gb) to Mebibyte (MiB)
    :param gb: Gigabytes (Gb)
    :return: Mebibytes (MiB)
    """
    return gb * 953.674


def gb_to_gib(gb: Union[int, float]) -> float:
    """
    Gigabyte (Gb) to Gibibyte (GiB)
    :param gb: Gigabytes (Gb)
    :return: Gibibyte (GiB)
    """
    return gb * 1.07374


def gib_to_mib(gib: Union[int, float]) -> float:
    """
    Gibibyte (GiB) to Mebibytes (GiB)
    :param gib: Gibibyte (GiB)
    :return: Mebibytes (MiB)
    """
    return gib * 1024.0


@total_ordering
class AWSBatchJobStates(enum.Enum):
    SUBMITTED = 1
    PENDING = 2
    RUNNABLE = 3
    STARTING = 4
    RUNNING = 5
    SUCCEEDED = 6
    FAILED = 7

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


@dataclass
class AWSBatchJobDescription:
    jobName: str = None
    jobId: str = None
    jobQueue: str = None
    status: str = None
    attempts: List[Dict] = None
    statusReason: str = None
    createdAt: int = None
    startedAt: int = None
    stoppedAt: int = None
    dependsOn: List[str] = None
    jobDefinition: str = None
    parameters: Dict = None
    container: Dict = None
    timeout: Dict = None
