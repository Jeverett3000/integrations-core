# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from os import path

HERE = path.dirname(path.abspath(__file__))

CHECK_NAME = 'cassandra_nodetool'

CASSANDRA_CONTAINER_NAME = 'dd-test-cassandra'
CASSANDRA_CONTAINER_NAME_2 = 'dd-test-cassandra2'

CONFIG_INSTANCE = {
    'nodetool': f'docker exec {CASSANDRA_CONTAINER_NAME} nodetool',
    'keyspaces': ['system', 'test'],
    'username': 'controlRole',
    'password': 'QED',
    'tags': ['foo', 'bar'],
}

PORT = "7199"
