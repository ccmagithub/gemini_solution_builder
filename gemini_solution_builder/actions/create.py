#    Copyright 2015 GeminiOpenCloud.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging
import os
import re

from gemini_solution_builder.actions import BaseAction
from gemini_solution_builder import consts
from gemini_solution_builder import errors
from gemini_solution_builder import messages
from gemini_solution_builder import utils
from gemini_solution_builder import version_mapping

logger = logging.getLogger(__name__)


class CreatePlugin(BaseAction):

    solution_name_pattern = re.compile(consts.SOLUTION_NAME_PATTERN)

    def __init__(self, solution_path, package_version=None):
        self.solution_name = utils.basename(solution_path.rstrip('/'))
        self.solution_path = solution_path
        self.package_version = (package_version or
                                version_mapping.latest_version)

        self.render_ctx = {'solution_name': self.solution_name}
        self.template_paths = version_mapping.get_solution_for_version(
            self.package_version)['templates']

    def check(self):
        if utils.exists(self.solution_path):
            raise errors.PluginDirectoryExistsError(
                'Plugins directory {0} already exists, '
                'choose another name'.format(self.solution_path))

        if not self.solution_name_pattern.match(self.solution_name):
            raise errors.ValidationError(
                messages.SOLUTION_WRONG_NAME_EXCEPTION_MESSAGE)

    def run(self):
        logger.debug('Start solution creation "%s"', self.solution_path)
        self.check()

        for template_path in self.template_paths:

            template_dir = os.path.join(
                os.path.dirname(__file__), '..', template_path)

            utils.copy(template_dir, self.solution_path)
            utils.render_files_in_dir(self.solution_path, self.render_ctx)
