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


from os.path import join as join_path

from gemini_solution_builder import errors
from gemini_solution_builder import utils


latest_version = '1.0.0'


def get_mapping():
    # NOTE(eli): It's required not to have circular dependencies error
    from gemini_solution_builder.actions import build
    from gemini_solution_builder import validators

    return [
        {'version': '1.0.0',
         'templates': ['templates/base', 'templates/v1/'],
         'validator': validators.ValidatorV1,
         'builder': build.BuildSolutionV1},
    ]


def get_solution_for_version(version):
    """Retrieves data which are required for specific version of solution

    :param str version: version of package
    :returns: dict which contains
              'version' - package version
              'templates' - array of paths to templates
              'validator' - validator class
              'builder' - builder class
    """
    data = filter(lambda p: p['version'] == version, get_mapping())

    if not data:
        raise errors.WrongPackageVersionError(
            'Wrong package version "{0}"'.format(version))

    return data[0]


def get_version_mapping_from_solution(solution_path):
    """Returns mapping for specific version of the solution

    :param str solution_path: path to the directory with metadata.yaml file
    :returns: dict which contains
              'version' - package version
              'validator' - validator class
              'templates' - path to templates
              'builder' - builder class
    """
    meta_path = join_path(solution_path, 'metadata.yaml')
    if not utils.exists(meta_path):
        errors.WrongSolutionDirectoryError(
            'Wrong path to the solution, cannot find "%s" file', meta_path)
        raise Exception('cannot find %s file' % meta_path)

    site_path = join_path(solution_path, 'site.yaml')
    if not utils.exists(site_path):
        errors.WrongSolutionDirectoryError(
            'Wrong path to the solution, cannot find "%s" file', site_path)
        raise Exception('cannot find %s file' % site_path)

    meta = utils.parse_yaml(meta_path)
    package_version = meta.get('version')

    return get_solution_for_version(package_version)
