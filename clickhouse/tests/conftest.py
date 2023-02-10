# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from copy import deepcopy

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckDockerLogs, CheckEndpoints

from . import common


@pytest.fixture(scope='session')
def dd_environment():
    conditions = []
    for i in range(6):
        conditions.extend(
            (
                CheckEndpoints(
                    [f'http://{common.HOST}:{common.HTTP_START_PORT + i}']
                ),
                CheckDockerLogs(
                    f'clickhouse-0{i + 1}',
                    'Logging errors to /var/log/clickhouse-server/clickhouse-server.err.log',
                ),
            )
        )
    with docker_run(common.COMPOSE_FILE, conditions=conditions, sleep=10, attempts=2):
        yield common.CONFIG


@pytest.fixture
def instance():
    return deepcopy(common.CONFIG)
