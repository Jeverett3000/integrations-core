# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import pytest

from datadog_checks.consul import ConsulCheck
from datadog_checks.dev.utils import get_metadata_metrics

from . import common
from .test_integration import MULTI_NODE_METRICS

pytestmark = pytest.mark.e2e


def test_e2e(dd_agent_check, instance_single_node_install):
    aggregator = dd_agent_check(instance_single_node_install, rate=True)

    aggregator.assert_metric('consul.peers', count=2)
    aggregator.assert_metric('consul.catalog.nodes_critical', count=2)
    aggregator.assert_metric('consul.catalog.services_passing', count=6)
    aggregator.assert_metric('consul.catalog.nodes_warning', count=2)
    aggregator.assert_metric('consul.catalog.services_warning', count=6)
    aggregator.assert_metric('consul.catalog.services_critical', count=6)
    aggregator.assert_metric('consul.catalog.services_up', count=6)
    aggregator.assert_metric('consul.catalog.nodes_passing', count=2)
    aggregator.assert_metric('consul.catalog.nodes_up', count=2)
    aggregator.assert_metric('consul.catalog.total_nodes', count=2)
    aggregator.assert_metric('consul.catalog.services_count', count=6)

    for metric in MULTI_NODE_METRICS:
        aggregator.assert_metric(metric, tags=['consul_datacenter:dc1'], at_least=0)

    aggregator.assert_service_check(
        'consul.up',
        ConsulCheck.OK,
        tags=[
            'consul_datacenter:dc1',
            f'consul_url:http://{common.HOST}:8500',
        ],
    )
    aggregator.assert_service_check(
        'consul.check',
        ConsulCheck.OK,
        tags=['check:serfHealth', 'consul_datacenter:dc1', 'consul_node:node-consul-follower-1'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/status/leader'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/status/peers'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/agent/self'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/health/state/any'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/catalog/services'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/catalog/nodes'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/coordinate/datacenters'],
    )
    aggregator.assert_service_check(
        'consul.can_connect',
        ConsulCheck.OK,
        tags=[f'url:http://{common.HOST}:8500/v1/coordinate/nodes'],
    )
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_all_metrics_covered()
