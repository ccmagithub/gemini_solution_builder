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


import argparse
import logging
import six
import sys

from gemini_solution_builder import actions
from gemini_solution_builder import errors
from gemini_solution_builder import messages
from gemini_solution_builder.validators import ValidatorManager
from gemini_solution_builder.common import utils

from gemini_solution_builder.logger import configure_logger

logger = logging.getLogger(__name__)


def print_err(line):
    sys.stderr.write(six.text_type(line))
    sys.stderr.write('\n')


def handle_exception(exc):
    logger.exception(exc)

    if isinstance(exc, errors.CannotFindCommandError):
        print_err(messages.HEADER)
        print_err(messages.INSTALL_REQUIRED_PACKAGES)

    elif isinstance(exc, errors.ValidationError):
        print_err('Validation failed')
        print_err(exc)

    else:
        print_err('Unexpected error')
        print_err(exc)

    sys.exit(-1)


def decode_string(string):
    """Custom type for add_argument method
    """
    return unicode(string, 'utf-8')


def parse_args():
    """Parse arguments and return them
    """
    parser = argparse.ArgumentParser(
        description='gsb is a gemini solution which '
        'helps you create solution for gemini cloud')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--create', help='create a solution skeleton',
        type=decode_string, metavar='solution_name')
    group.add_argument(
        '--build', help='build a solution',
        type=decode_string, metavar='path_to_directory')
    group.add_argument(
        '--check', help='check that solution is valid',
        type=decode_string, metavar='path_to_directory')
    # group.add_argument(
    #     '--upload', help='upload a solution',
    #     type=decode_string, metavar='path_to_package')
    # group.add_argument(
    #     '--list', help='list a solution', action='store_true')
    # group.add_argument(
    #     '--delete', help='delete a solution',
    #     type=decode_string, metavar='solution_id')
    parser.add_argument(
        '--debug', help='enable debug mode',
        action="store_true")

    parser.add_argument(
        '--package-version', help='which package version to use',
        type=decode_string)

    # ex. admin
    # parser.add_argument(
    #     '--username', default=utils.env('GOC_USERNAME'),
    #     help='Defaults to env[GOC_USERNAME].')

    # ex. admin
    # parser.add_argument(
    #     '--password', default=utils.env('GOC_PASSWORD'),
    #     help='Defaults to env[GOC_PASSWORD].')

    # ex. http://10.14.1.13:8000/api/
    # parser.add_argument(
    #     '--api-url', default=utils.env('GOC_API_URL'),
    #     help='Defaults to env[GOC_API_URL].')

    result = parser.parse_args()
    package_version_check(result, parser)

    return result


def perform_action(args):
    """Performs an action

    :param args: argparse object
    """
    if args.create:
        actions.CreateSolution(args.create, args.package_version).run()
        print('Solution is created')
    elif args.build:
        actions.make_builder(args.build).run()
        print('Solution is built')
    elif args.check:
        ValidatorManager(args.check).get_validator().validate()
        print('Solution is valid')
    elif args.upload:
        actions.UploadSolution(args.upload, args.username, args.password,
                               args.api_url).run()
    elif args.list:
        actions.ListSolution(args.username, args.password,
                             args.api_url).run()
    elif args.delete:
        actions.DeleteSolution(args.delete, args.username, args.password,
                               args.api_url).run()


def package_version_check(args, parser):
    """Check exclusive nature of --package-version argument
    """
    if (args.build or args.check) and args.package_version:
        parser.error('--package-version works only with --create')


def main():
    """Entry point
    """
    try:
        args = parse_args()
        configure_logger(debug=args.debug)
        perform_action(args)
    except Exception as exc:
        handle_exception(exc)
