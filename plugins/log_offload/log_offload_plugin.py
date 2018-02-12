# -*- coding: utf-8 -*-
# Copyright 2018 GIG Technology NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.4@@
from google.appengine.ext import ndb

from config import LogOffloadConfig
from framework.plugin_loader import Plugin
from framework.utils.plugins import Handler
from handlers import ExportLogsHandler
from log_offload.consts import OFFLOAD_HEADER
from log_offload.log_offload import LogOffload
from log_offload.models import OffloadSettings, OffloadRun
from mcfw.consts import DEBUG, MISSING

OFFLOAD_PLUGIN_NAME = 'log_offload'


class LogOffloadPlugin(Plugin):
    def __init__(self, configuration):
        super(LogOffloadPlugin, self).__init__(LogOffloadConfig.from_dict(configuration))
        assert isinstance(self.configuration, LogOffloadConfig)
        if not self.configuration.offload_header or self.configuration.offload_header is MISSING:
            self.configuration.offload_header = OFFLOAD_HEADER
        if DEBUG:
            OffloadSettings.get_instance(OFFLOAD_PLUGIN_NAME).key.delete()
            ndb.delete_multi(OffloadRun.query(namespace=OFFLOAD_PLUGIN_NAME).fetch(keys_only=True))
        self.log_offload = LogOffload(self.configuration.cloudstorage_bucket, self.configuration.application_name,
                                      offload_header=self.configuration.offload_header, namespace=OFFLOAD_PLUGIN_NAME)

    def get_handlers(self, auth):
        if auth == Handler.AUTH_ADMIN:
            yield Handler('/admin/cron/log_offload/export', ExportLogsHandler)

    def create_log(self, user, type_, request_data, response_data, function_=None, success=None):
        # type: (unicode, unicode, dict, dict, unicode, bool) -> None
        self.log_offload.create_log(user, type_, request_data, response_data, function_, success)

    def export_logs(self):
        self.log_offload.export_logs()
