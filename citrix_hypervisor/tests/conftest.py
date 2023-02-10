# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import mock
import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.http import MockResponse

from . import common


@pytest.fixture(scope='session')
def dd_environment():
    with docker_run(common.COMPOSE_FILE, endpoints=[f"{common.E2E_INSTANCE[0]['url']}/rrd_updates", f"{common.E2E_INSTANCE[1]['url']}/rrd_updates", f"{common.E2E_INSTANCE[2]['url']}/rrd_updates"]):
        yield common.E2E_INSTANCE


@pytest.fixture
def instance():
    return common.MOCKED_INSTANCE


def mock_requests_get(url, *args, **kwargs):
    url_parts = url.split('/')

    if url_parts[0] != 'mocked':
        return MockResponse(status_code=404)

    path = os.path.join(
        common.HERE, 'fixtures', 'standalone', f'{url_parts[1]}.json'
    )
    return (
        MockResponse(file_path=path)
        if os.path.exists(path)
        else MockResponse(status_code=404)
    )


@pytest.fixture
def mock_responses():
    with mock.patch('requests.get', side_effect=mock_requests_get):
        yield
