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

from framework.plugin_loader import Plugin
from log_offload.log_offload import LogOffload

OFFLOAD_PLUGIN_NAME = 'log_offload'


class LogOffloadPlugin(Plugin):
    def __init__(self, configuration):
        super(LogOffloadPlugin, self).__init__(configuration)
        self.log_offload = LogOffload()

    def create_log(self, user, type_, request_data, response_data, function_=None, success=None):
        # type: (unicode, unicode, dict, dict, unicode, bool) -> None
        self.log_offload.create_log(user, type_, request_data, response_data, function_, success)
