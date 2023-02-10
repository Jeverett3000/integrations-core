# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import re

from six import iteritems

from datadog_checks.base.utils.containers import hash_mutable

from . import exceptions, helpers

TN_REGEX = re.compile('/tn-([^/]+)/')
APP_REGEX = re.compile('/ap-([^/]+)/')


class CiscoTags:
    def __init__(self, log=None):
        self.tenant_farbic_mapper = {}
        self.tenant_tags = {}
        self._api = None
        if log:
            self.log = log
        else:
            import logging

            self.log = logging.getLogger('cisco_api')

    def _app_tags(self, app):
        tags = []
        if not app or type(app) is not dict:
            return tags
        attrs = app.get('attributes', {})
        if type(attrs) is not dict:
            return tags
        app_name = attrs.get('name')
        dn = attrs.get('dn')
        if app_name:
            tags.append(f"application:{app_name}")
        if dn:
            if tenant := re.search(TN_REGEX, dn):
                tags.append(f"tenant:{tenant[1]}")
        return tags

    def _edpt_tags_map(self, edpt):
        tags_map = {}
        if not edpt or type(edpt) is not dict:
            return tags_map
        attrs = edpt.get('attributes', {})
        if type(attrs) is not dict:
            return tags_map
        epg_name = attrs.get('name')
        dn = attrs.get('dn')
        if epg_name:
            tags_map["endpoint_group"] = f"{epg_name}"
        if dn:
            if tenant := re.search(TN_REGEX, dn):
                tenant_name = tenant[1]
                tags_map["tenant"] = tenant_name

            if app := re.search(APP_REGEX, dn):
                app_name = app[1]
                tags_map["application"] = app_name
        return tags_map

    def _epg_meta_tags_map(self, epg_meta):
        tags_map = {}
        if not epg_meta or type(epg_meta) is not dict:
            return tags_map
        attrs = epg_meta.get('attributes', {})
        if type(attrs) is not dict:
            return tags_map
        if ip := attrs.get('ip'):
            tags_map["ip"] = ip
        if mac := attrs.get('mac'):
            tags_map["mac"] = mac
        if encap := attrs.get('encap'):
            tags_map["encap"] = encap
        return tags_map

    def _get_epg_meta_tags_map(self, tenant_name, app_name, epg_name):
        try:
            epg_metas = self.api.get_epg_meta(tenant_name, app_name, epg_name)
            if len(epg_metas) > 0 and epg_metas[0] and type(epg_metas[0]) is dict:
                epg = epg_metas[0].get('fvCEp', {})
                return self._epg_meta_tags_map(epg)
        except (exceptions.APIConnectionException, exceptions.APIParsingException):
            # the exception will already be logged, just pass it over here
            pass
        return {}

    def _tenant_mapper(self, edpt):
        tags = []
        if not edpt or type(edpt) is not dict:
            return tags

        application_meta_map = self._edpt_tags_map(edpt)
        application_meta = [f"{k}:{v}" for k, v in iteritems(application_meta_map)]
        tenant_name = application_meta_map.get("tenant")
        app_name = application_meta_map.get("application")
        epg_name = application_meta_map.get("endpoint_group")

        endpoint_meta_map = self._get_epg_meta_tags_map(tenant_name, app_name, epg_name)
        endpoint_meta = [f"{k}:{v}" for k, v in iteritems(endpoint_meta_map)]
        # adding application tags
        endpoint_meta += application_meta

        context_hash = hash_mutable(endpoint_meta)
        eth_meta = []
        if self.tenant_tags.get(context_hash):
            eth_meta = self.tenant_tags.get(context_hash)
        else:
            try:
                # adding eth and node tags
                eth_list = self.api.get_eth_list_for_epg(tenant_name, app_name, epg_name)
                for eth in eth_list:
                    eth_attrs = eth.get('fvRsCEpToPathEp', {}).get('attributes', {})
                    port = re.search(r'/pathep-\[(.+?)\]', eth_attrs.get('tDn', ''))
                    if not port:
                        continue
                    eth_tag = f'port:{port[1]}'
                    if eth_tag not in eth_meta:
                        eth_meta.append(eth_tag)
                    node = re.search('/paths-(.+?)/', eth_attrs.get('tDn', ''))
                    if not node:
                        continue
                    eth_node = f'node_id:{node[1]}'
                    if eth_node not in eth_meta:
                        eth_meta.append(eth_node)
                    # populating the map for eth-app mapping

                    tenant_fabric_key = f"{node[1]}:{port[1]}"
                    if tenant_fabric_key not in self.tenant_farbic_mapper:
                        self.tenant_farbic_mapper[tenant_fabric_key] = application_meta
                    else:
                        self.tenant_farbic_mapper[tenant_fabric_key].extend(application_meta)

                    self.tenant_farbic_mapper[tenant_fabric_key] = list(
                        set(self.tenant_farbic_mapper[tenant_fabric_key])
                    )
            except (exceptions.APIConnectionException, exceptions.APIParsingException):
                # the exception will already be logged, just pass it over here
                pass

        tags = tags + endpoint_meta + eth_meta
        if len(eth_meta) > 0:
            self.log.debug('adding eth level tags: %s', eth_meta)
        return tags

    def get_endpoint_group_tags(self, obj):
        return self._tenant_mapper(obj)

    def get_application_tags(self, obj):
        return self._app_tags(obj)

    def get_fabric_tags(self, obj, obj_type):
        tags = []
        if not obj or type(obj) is not dict:
            return tags
        obj = helpers.get_attributes(obj)
        if obj_type == 'fabricNode':
            if obj.get('role') and obj.get('role') != "controller":
                tags.append("switch_role:" + obj.get('role'))
            if obj.get('role'):
                tags.append("apic_role:" + obj.get('role'))
            if obj.get('id'):
                tags.append("node_id:" + obj.get('id'))
            if obj.get('fabricSt'):
                tags.append("fabric_state:" + obj.get('fabricSt'))
            if helpers.get_pod_from_dn(obj.get('dn')):
                tags.append("fabric_pod_id:" + helpers.get_pod_from_dn(obj.get('dn')))
        if obj_type == 'fabricPod' and obj.get('id'):
            tags.append("fabric_pod_id:" + obj.get('id'))
        if obj_type == 'l1PhysIf':
            if obj.get('id'):
                tags.append("port:" + obj.get('id'))
            if obj.get('medium'):
                tags.append("medium:" + obj.get('medium'))
            if obj.get('snmpTrapSt'):
                tags.append("snmpTrapSt:" + obj.get('snmpTrapSt'))
            node_id = helpers.get_node_from_dn(obj.get('dn'))
            pod_id = helpers.get_pod_from_dn(obj.get('dn'))
            if node_id:
                tags.append(f"node_id:{node_id}")
            if pod_id:
                tags.append(f"fabric_pod_id:{pod_id}")
            key = f"{node_id}:" + obj.get('id')
            if key in self.tenant_farbic_mapper.keys():
                tags += self.tenant_farbic_mapper[key]
        return tags

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value
