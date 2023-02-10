# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.dev import get_docker_hostname

CHECK_NAME = 'coredns'
NAMESPACE = 'coredns'

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
ATHOST = f"@{HOST}"
PORT = '9153'
URL = f"http://{HOST}:{PORT}/metrics"

COREDNS_VERSION = [int(i) for i in os.environ['COREDNS_VERSION'].split(".")]

CONFIG_FILE = os.path.join(HERE, 'docker', 'coredns', 'Corefile-v1.%d' % COREDNS_VERSION[1])

COMMON_METRICS = [
    f'{NAMESPACE}.build_info',
    f'{NAMESPACE}.go.gc_duration_seconds.count',
    f'{NAMESPACE}.go.gc_duration_seconds.quantile',
    f'{NAMESPACE}.go.gc_duration_seconds.sum',
    f'{NAMESPACE}.go.goroutines',
    f'{NAMESPACE}.go.memstats.alloc_bytes',
    f'{NAMESPACE}.go.memstats.alloc_bytes_total',
    f'{NAMESPACE}.go.memstats.buck_hash_sys_bytes',
    f'{NAMESPACE}.go.memstats.frees_total',
    f'{NAMESPACE}.go.memstats.gc_sys_bytes',
    f'{NAMESPACE}.go.memstats.heap_alloc_bytes',
    f'{NAMESPACE}.go.memstats.heap_idle_bytes',
    f'{NAMESPACE}.go.memstats.heap_inuse_bytes',
    f'{NAMESPACE}.go.memstats.heap_objects',
    f'{NAMESPACE}.go.memstats.heap_sys_bytes',
    f'{NAMESPACE}.go.memstats.last_gc_time_seconds',
    f'{NAMESPACE}.go.memstats.lookups_total',
    f'{NAMESPACE}.go.memstats.mallocs_total',
    f'{NAMESPACE}.go.memstats.mcache_inuse_bytes',
    f'{NAMESPACE}.go.memstats.mcache_sys_bytes',
    f'{NAMESPACE}.go.memstats.mspan_inuse_bytes',
    f'{NAMESPACE}.go.memstats.mspan_sys_bytes',
    f'{NAMESPACE}.go.memstats.next_gc_bytes',
    f'{NAMESPACE}.go.memstats.other_sys_bytes',
    f'{NAMESPACE}.go.memstats.stack_inuse_bytes',
    f'{NAMESPACE}.go.memstats.stack_sys_bytes',
    f'{NAMESPACE}.go.memstats.sys_bytes',
    f'{NAMESPACE}.health_request_duration.count',
    f'{NAMESPACE}.health_request_duration.sum',
    f'{NAMESPACE}.panic_count.count',
    f'{NAMESPACE}.process.cpu_seconds_total',
    f'{NAMESPACE}.process.max_fds',
    f'{NAMESPACE}.process.open_fds',
    f'{NAMESPACE}.process.resident_memory_bytes',
    f'{NAMESPACE}.process.start_time_seconds',
    f'{NAMESPACE}.process.virtual_memory_bytes',
    f'{NAMESPACE}.request_count',
    f'{NAMESPACE}.cache_size.count',
    f'{NAMESPACE}.cache_misses_count',
    f'{NAMESPACE}.response_code_count',
    f'{NAMESPACE}.response_size.bytes.sum',
    f'{NAMESPACE}.response_size.bytes.count',
    f'{NAMESPACE}.request_size.bytes.sum',
    f'{NAMESPACE}.request_size.bytes.count',
    f'{NAMESPACE}.request_duration.seconds.sum',
    f'{NAMESPACE}.request_duration.seconds.count',
    f'{NAMESPACE}.forward_request_count',
    f'{NAMESPACE}.forward_request_duration.seconds.sum',
    f'{NAMESPACE}.forward_request_duration.seconds.count',
    f'{NAMESPACE}.forward_response_rcode_count',
]

COMMON_METRICS_OMV2 = [
    f'{NAMESPACE}.build_info',
    f'{NAMESPACE}.go.gc_duration_seconds.count',
    f'{NAMESPACE}.go.gc_duration_seconds.quantile',
    f'{NAMESPACE}.go.gc_duration_seconds.sum',
    f'{NAMESPACE}.go.goroutines',
    f'{NAMESPACE}.go.memstats.alloc_bytes',
    f'{NAMESPACE}.go.memstats.buck_hash_sys_bytes',
    f'{NAMESPACE}.go.memstats.frees_total.count',
    f'{NAMESPACE}.go.memstats.gc_sys_bytes',
    f'{NAMESPACE}.go.memstats.heap_alloc_bytes',
    f'{NAMESPACE}.go.memstats.heap_idle_bytes',
    f'{NAMESPACE}.go.memstats.heap_inuse_bytes',
    f'{NAMESPACE}.go.memstats.heap_objects',
    f'{NAMESPACE}.go.memstats.heap_sys_bytes',
    f'{NAMESPACE}.go.memstats.last_gc_time_seconds',
    f'{NAMESPACE}.go.memstats.lookups_total.count',
    f'{NAMESPACE}.go.memstats.mallocs_total.count',
    f'{NAMESPACE}.go.memstats.mcache_inuse_bytes',
    f'{NAMESPACE}.go.memstats.mcache_sys_bytes',
    f'{NAMESPACE}.go.memstats.mspan_inuse_bytes',
    f'{NAMESPACE}.go.memstats.mspan_sys_bytes',
    f'{NAMESPACE}.go.memstats.next_gc_bytes',
    f'{NAMESPACE}.go.memstats.other_sys_bytes',
    f'{NAMESPACE}.go.memstats.stack_inuse_bytes',
    f'{NAMESPACE}.go.memstats.stack_sys_bytes',
    f'{NAMESPACE}.go.memstats.sys_bytes',
    f'{NAMESPACE}.health_request_duration.count',
    f'{NAMESPACE}.health_request_duration.sum',
    f'{NAMESPACE}.health_request_duration.bucket',
    f'{NAMESPACE}.panic_count.count',
    f'{NAMESPACE}.process.cpu_seconds_total.count',
    f'{NAMESPACE}.process.max_fds',
    f'{NAMESPACE}.process.open_fds',
    f'{NAMESPACE}.process.resident_memory_bytes',
    f'{NAMESPACE}.process.start_time_seconds',
    f'{NAMESPACE}.process.virtual_memory_bytes',
    f'{NAMESPACE}.request_count.count',
    f'{NAMESPACE}.cache_size.count',
    f'{NAMESPACE}.cache_misses_count.count',
    f'{NAMESPACE}.response_code_count.count',
    f'{NAMESPACE}.response_size.bytes.sum',
    f'{NAMESPACE}.response_size.bytes.count',
    f'{NAMESPACE}.response_size.bytes.bucket',
    f'{NAMESPACE}.request_size.bytes.sum',
    f'{NAMESPACE}.request_size.bytes.count',
    f'{NAMESPACE}.request_size.bytes.bucket',
    f'{NAMESPACE}.request_duration.seconds.sum',
    f'{NAMESPACE}.request_duration.seconds.count',
    NAMESPACE + '.request_duration.seconds.bucket',
    NAMESPACE + '.forward_request_count.count',
    NAMESPACE + '.forward_request_duration.seconds.sum',
    NAMESPACE + '.forward_request_duration.seconds.count',
    NAMESPACE + '.forward_request_duration.seconds.bucket',
    NAMESPACE + '.forward_response_rcode_count.count',
]

METRICS_V1_2 = COMMON_METRICS + [
    # Has been removed from v1.7.0
    NAMESPACE + '.request_type_count',
    # The proxy plugin has been deprecated
    NAMESPACE + '.proxy_request_count',
    NAMESPACE + '.proxy_request_duration.seconds.sum',
    NAMESPACE + '.proxy_request_duration.seconds.count',
    NAMESPACE + '.forward_sockets_open',
]

METRICS_V1_2_OMV2 = COMMON_METRICS_OMV2 + [
    # Has been removed from v1.7.0
    NAMESPACE + '.request_type_count.count',
    NAMESPACE + '.proxy_request_count.count',
    NAMESPACE + '.proxy_request_duration.seconds.bucket',
    # The proxy plugin has been deprecated
    NAMESPACE + '.proxy_request_duration.seconds.sum',
    NAMESPACE + '.proxy_request_duration.seconds.count',
    NAMESPACE + '.forward_sockets_open',
    NAMESPACE + '.go.memstats.heap_released_bytes.count',
]

METRICS_V1_8 = COMMON_METRICS + [
    NAMESPACE + '.forward_max_concurrent_rejects',
    NAMESPACE + '.go.info',
    NAMESPACE + '.go.memstats.gc_cpu_fraction',
    NAMESPACE + '.go.memstats.heap_released_bytes',
    NAMESPACE + '.cache_request_count',
    NAMESPACE + '.plugin_enabled',
    NAMESPACE + '.forward_healthcheck_broken_count',
    NAMESPACE + '.hosts.reload_timestamp',
    NAMESPACE + '.reload.failed_count',
]

METRICS_V1_8_OMV2 = COMMON_METRICS_OMV2 + [
    NAMESPACE + '.forward_max_concurrent_rejects.count',
    NAMESPACE + '.go.info',
    NAMESPACE + '.go.memstats.gc_cpu_fraction',
    NAMESPACE + '.go.memstats.heap_released_bytes',
    NAMESPACE + '.cache_request_count.count',
    NAMESPACE + '.plugin_enabled',
    NAMESPACE + '.forward_healthcheck_broken_count.count',
    NAMESPACE + '.hosts.reload_timestamp',
    NAMESPACE + '.reload.failed_count.count',
]

METRICS = METRICS_V1_8 if COREDNS_VERSION[:2] == [1, 8] else METRICS_V1_2

METRICS_V2 = METRICS_V1_8_OMV2 if COREDNS_VERSION[:2] == [1, 8] else METRICS_V1_2_OMV2
