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
import json

from gemini_solution_builder.actions import BaseAction
from gemini_solution_builder import consts
from gemini_solution_builder import errors
from gemini_solution_builder import messages
from gemini_solution_builder import utils
from gemini_solution_builder.common.utils import print_list
from gemini_solution_builder.common.utils import Model

logger = logging.getLogger(__name__)


class ListSolution(BaseAction):

    solution_name_pattern = re.compile(consts.SOLUTION_NAME_PATTERN)

    def __init__(self, username, password,
                 api_url):
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
        logger.debug('Start listing solutions')
        logger.debug('username: %s', self.username)
        logger.debug('pass: %s', self.password)
        logger.debug('url: %s', self.api_url)
        url = self.api_url+'/solutions/'
        r = requests.get(url, auth=(self.username, self.password),
                         verify=False)
        sol_json = json.loads(r.text)
        solutions = []
        for s in sol_json:
            solutions.append(Model(**s))
        print_list(solutions,
                   ['id', 'name', 'state', 'desc', 'is_enabled', 'category'],
                   order_by='id')
