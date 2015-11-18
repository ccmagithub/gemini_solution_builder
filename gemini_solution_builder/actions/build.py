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


from __future__ import unicode_literals

import abc
import logging
import os

from os.path import join as join_path

from gemini_solution_builder.actions import BaseAction
from gemini_solution_builder import errors
from gemini_solution_builder import utils
from gemini_solution_builder.validators import ValidatorManager
from gemini_solution_builder import version_mapping


logger = logging.getLogger(__name__)


class BaseBuildSolution(BaseAction):

    @abc.abstractproperty
    def requires(self):
        """Should return a list of commands which
        are required for the builder
        """

    @abc.abstractproperty
    def result_package_mask(self):
        """Should return mask for built package
        """

    @abc.abstractmethod
    def make_package(self):
        """Method should be implemented in child classes
        """

    def __init__(self, solution_path):
        self.solution_path = solution_path

        self.pre_build_hook_path = join_path(self.solution_path,
                                             'pre_build_hook')
        self.meta = utils.parse_yaml(
            join_path(self.solution_path, 'metadata.yaml')
        )
        self.build_dir = join_path(self.solution_path, '.build')
        self.build_src_dir = join_path(self.build_dir, 'src')
        self.checksums_path = join_path(self.build_src_dir, 'checksums.sha1')
        self.name = self.meta['name']

    def run(self):
        logger.debug('Start solution building "%s"', self.solution_path)
        self.clean()
        self.run_pre_build_hook()
        self.check()
        self.build_repos()
        self.add_checksums_file()
        self.make_package()

    def clean(self):
        utils.remove(self.build_dir)
        utils.create_dir(self.build_dir)
        utils.remove_by_mask(self.result_package_mask)

    def run_pre_build_hook(self):
        if utils.which(self.pre_build_hook_path):
            utils.exec_cmd(self.pre_build_hook_path)

    def add_checksums_file(self):
        utils.create_checksums_file(self.build_src_dir, self.checksums_path)

    def build_repos(self):
        utils.create_dir(self.build_src_dir)

        utils.copy_files_in_dir(
            join_path(self.solution_path, '*'),
            self.build_src_dir)

        releases_paths = {}
        for release in self.meta['releases']:
            releases_paths.setdefault(release['os'], [])
            releases_paths[release['os']].append(
                join_path(self.build_src_dir, release['repository_path']))

        self.build_ubuntu_repos(releases_paths.get('ubuntu', []))
        self.build_centos_repos(releases_paths.get('centos', []))

    def build_ubuntu_repos(cls, releases_paths):
        for repo_path in releases_paths:
            utils.exec_piped_cmds(
                ['dpkg-scanpackages .', 'gzip -c9 > Packages.gz'],
                cwd=repo_path)

    @classmethod
    def build_centos_repos(cls, releases_paths):
        for repo_path in releases_paths:
            repo_packages = join_path(repo_path, 'Packages')
            utils.create_dir(repo_packages)
            utils.move_files_in_dir(
                join_path(repo_path, '*.rpm'),
                repo_packages)
            utils.exec_cmd('createrepo -o {0} {0}'.format(repo_path))

    def check(self):
        self._check_requirements()
        self._check_structure()

    def _check_requirements(self):
        not_found = filter(lambda r: not utils.which(r), self.requires)

        if not_found:
            raise errors.CannotFindCommandError(
                'Cannot find commands "{0}", '
                'install required commands and try again'.format(
                    ', '.join(not_found)))

    def _check_structure(self):
        ValidatorManager(self.solution_path).get_validator().validate()


class BuildSolutionV1(BaseBuildSolution):

    requires = ['rpm', 'createrepo', 'dpkg-scanpackages']

    @property
    def result_package_mask(self):
        return join_path(self.solution_path, '{0}-*.fp'.format(self.name))

    def make_package(self):
        full_name = '{0}-{1}'.format(self.meta['name'],
                                     self.meta['version'])
        tar_name = '{0}.fp'.format(full_name)
        tar_path = join_path(
            self.solution_path,
            tar_name)

        utils.make_tar_gz(self.build_src_dir, tar_path, full_name)


class BuildSolutionV2(BaseBuildSolution):

    requires = ['rpmbuild', 'rpm', 'createrepo', 'dpkg-scanpackages']

    rpm_spec_src_path = 'templates/v2/build/solution_rpm.spec.mako'
    release_tmpl_src_path = 'templates/v2/build/Release.mako'

    def __init__(self, *args, **kwargs):
        super(BuildSolutionV2, self).__init__(*args, **kwargs)

        self.solution_version, self.full_version = \
            utils.version_split_name_rpm(self.meta['version'])

        self.rpm_path = os.path.abspath(
            join_path(self.solution_path, '.build', 'rpm'))

        self.rpm_src_path = join_path(self.rpm_path, 'SOURCES')
        self.full_name = '{0}-{1}'.format(
            self.meta['name'], self.solution_version)

        tar_name = '{0}.fp'.format(self.full_name)
        self.tar_path = join_path(self.rpm_src_path, tar_name)

        fpb_dir = join_path(os.path.dirname(__file__), '..')

        self.spec_src = os.path.abspath(join_path(
            fpb_dir, self.rpm_spec_src_path))

        self.release_tmpl_src = os.path.abspath(join_path(
            fpb_dir, self.release_tmpl_src_path))

        self.spec_dst = join_path(self.rpm_path, 'solution_rpm.spec')

        self.rpm_packages_mask = join_path(
            self.rpm_path, 'RPMS', 'noarch', '*.rpm')

    @property
    def result_package_mask(self):
        return join_path(
            self.solution_path, '{0}-*.noarch.rpm'.format(self.name))

    def make_package(self):
        """Builds rpm package
        """
        utils.create_dir(self.rpm_src_path)

        utils.make_tar_gz(self.build_src_dir, self.tar_path, self.full_name)
        utils.render_to_file(
            self.spec_src,
            self.spec_dst,
            self._make_data_for_template())

        utils.exec_cmd(
            'rpmbuild -vv --nodeps --define "_topdir {0}" '
            '-bb {1}'.format(self.rpm_path, self.spec_dst))
        utils.copy_files_in_dir(self.rpm_packages_mask, self.solution_path)

    def _make_data_for_template(self):
        """Generates data for spec template

        :returns: dictionary with required data
        """
        return {
            'name': self.full_name,
            'version': self.full_version,
            'summary': self.meta['title'],
            'description': self.meta['description'],
            'license': ' and '.join(self.meta.get('licenses', [])),
            'homepage': self.meta.get('homepage'),
            'vendor': ', '.join(self.meta.get('authors', [])),
            'year': utils.get_current_year()}

    def build_ubuntu_repos(self, releases_paths):
        for repo_path in releases_paths:
            utils.exec_piped_cmds(
                ['dpkg-scanpackages .', 'gzip -c9 > Packages.gz'],
                cwd=repo_path)
            release_path = join_path(repo_path, 'Release')
            utils.render_to_file(
                self.release_tmpl_src,
                release_path,
                {'solution_name': self.meta['name'],
                 'major_version': self.solution_version})


class BuildSolutionV3(BuildSolutionV2):

    rpm_spec_src_path = 'templates/v3/build/solution_rpm.spec.mako'
    release_tmpl_src_path = 'templates/v3/build/Release.mako'

    def _make_data_for_template(self):
        data = super(BuildSolutionV3, self)._make_data_for_template()

        uninst = utils.read_if_exist(
            join_path(self.solution_path, "uninstall.sh"))

        preinst = utils.read_if_exist(
            join_path(self.solution_path, "pre_install.sh"))

        postinst = utils.read_if_exist(
            join_path(self.solution_path, "post_install.sh"))

        data.update(
            {'postinstall_hook': postinst,
             'preinstall_hook': preinst,
             'uninstall_hook': uninst}
        )

        return data


def make_builder(solution_path):
    """Creates build object

    :param str solution_path: path to the solution
    :returns: specific version of builder object
    """
    builder = version_mapping.get_version_mapping_from_solution(
        solution_path)['builder']

    return builder(solution_path)
