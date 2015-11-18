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


from gemini_solution_builder import version_mapping


class ValidatorManager(object):

    def __init__(self, solution_path):
        self.solution_path = solution_path

    def get_validator(self):
        validator = version_mapping.get_version_mapping_from_solution(
            self.solution_path)['validator']
        return validator(self.solution_path)
