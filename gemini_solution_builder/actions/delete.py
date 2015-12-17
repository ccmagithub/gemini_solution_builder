
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
import re
import requests

from gemini_solution_builder.actions import BaseAction
from gemini_solution_builder import consts
from gemini_solution_builder import errors
from gemini_solution_builder import messages
from gemini_solution_builder import utils

logger = logging.getLogger(__name__)


class DeleteSolution(BaseAction):

    solution_name_pattern = re.compile(consts.SOLUTION_NAME_PATTERN)

    def __init__(self, solution_id, username, password,
                 api_url):
        self.solution_id = solution_id
        self.username = username
        self.password = password
        self.api_url = api_url.strip('/')

    def check(self):
        if utils.exists(self.solution_path):
            raise errors.SolutionDirectoryExistsError(
                'Solutions directory {0} already exists, '
                'choose another name'.format(self.solution_path))

        if not self.solution_name_pattern.match(self.solution_name):
            raise errors.ValidationError(
                messages.SOLUTION_WRONG_NAME_EXCEPTION_MESSAGE)

    def run(self):
        logger.debug('Start solution deleting "%s"', self.solution_id)
        logger.debug('username: %s', self.username)
        logger.debug('pass: %s', self.password)
        logger.debug('url: %s', self.api_url)
        url = self.api_url+'/solutions/'+self.solution_id
        r = requests.delete(url, auth=(self.username, self.password),
                            verify=False)
        if r.status_code not in (200, 201, 204, 300):
            raise errors.SolutionUploadError(r.text)
        print "Success."
