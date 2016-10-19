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


class BaseSolutionException(Exception):
    pass


class CannotFindCommandError(BaseSolutionException):
    pass


class ExecutedErrorNonZeroExitCode(BaseSolutionException):
    pass


class SolutionDirectoryExistsError(BaseSolutionException):
    pass


class ValidationError(BaseSolutionException):
    pass


class FileIsEmpty(ValidationError):
    def __init__(self, file_path):
        super(FileIsEmpty, self).__init__(
            "File '{0}' is empty".format(file_path)
        )


class FileDoesNotExist(ValidationError):
    def __init__(self, file_path):
        super(FileDoesNotExist, self).__init__(
            "File '{0}' does not exist".format(file_path)
        )


class WrongPackageVersionError(BaseSolutionException):
    pass


class ReleasesDirectoriesError(BaseSolutionException):
    pass


class WrongSolutionDirectoryError(BaseSolutionException):
    pass


class SolutionUploadError(BaseSolutionException):
    pass
