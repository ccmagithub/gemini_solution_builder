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
import requests
import yaml
import json

from gemini_solution_builder.actions import BaseAction
from gemini_solution_builder import consts
from gemini_solution_builder import errors
from gemini_solution_builder import messages
from gemini_solution_builder import utils
from gemini_solution_builder.common import utils as comm_utils
from gemini_solution_builder.common.utils import Model

logger = logging.getLogger(__name__)


class UploadSolution(BaseAction):

    solution_name_pattern = re.compile(consts.SOLUTION_NAME_PATTERN)

    def __init__(self, solution_path, username, password,
                 api_url):
        self.solution_name = utils.basename(solution_path.rstrip('/'))
        self.solution_path = os.path.abspath(solution_path)
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

    def _get_categories(self):
        cat_url = self.api_url+'/categories/'
        r = requests.get(cat_url, auth=(self.username, self.password))
        cats = json.loads(r.text)
        categories = []
        for c in cats:
            Cate = Model(**c)
            categories.append(Cate)
        return categories

    def _solution_create(self, name, desc, category):
        url = self.api_url+'/solutions/'
        data = {"name": name, "desc": desc, "category": category}
        r = requests.post(url, auth=(self.username, self.password), data=data)
        if r.status_code not in (200, 201, 204, 300):
            raise errors.SolutionUploadError(r.text)
        sol = json.loads(r.text)
        solution = Model(**sol)
        return solution

    def _solution_upload(self, image_id):
        url = self.api_url + "/solutions/%s/file/" % image_id
        with open(self.solution_path, 'rb') as fh:
            files = {'data': fh}
            r = requests.put(url,
                             auth=(self.username, self.password),
                             files=files)
            if r.status_code not in (200, 201, 204, 300):
                raise errors.SolutionUploadError(r.text)

    def run(self):
        logger.debug('Start solution uploading "%s"', self.solution_path)
        logger.debug('username: %s', self.username)
        logger.debug('pass: %s', self.password)
        logger.debug('url: %s', self.api_url)
        file_name = self.solution_path
        if file_name is not None and os.access(file_name, os.R_OK) is False:
            raise errors.FileDoesNotExist(file_name)

        metafile = os.path.dirname(self.solution_path)+'/metadata.yaml'
        category = None
        with open(metafile, 'r') as f:
            meta = yaml.load(f)
            category = meta['category']
            meta_solname = meta['name']
            meta_description = meta['description']
        if category is None:
            logger.debug("Can't find category in metadata.yaml")
            raise errors.ValidationError()
        categories = self._get_categories()
        category_id = 0
        for cat in categories:
            if category == getattr(cat, 'name'):
                category_id = getattr(cat, 'id')
        if category_id == 0:
            logger.debug("Invalid category %s", category)
            raise errors.ValidationError()

        solution = self._solution_create(meta_solname, meta_description,
                                         category_id)
        self._solution_upload(solution.id)
        comm_utils.print_list(
            [solution],
            ['id', 'name', 'state', 'desc', 'is_enabled', 'category'],
            order_by='id')
