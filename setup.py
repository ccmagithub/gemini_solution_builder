#    Copyright 2015 GeminiOpenCloud, Inc.
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

import os

from setuptools import find_packages
from setuptools import setup


def find_requires():
    prj_root = os.path.dirname(os.path.realpath(__file__))
    requirements = []
    with open(u'{0}/requirements.txt'.format(prj_root), 'r') as reqs:
        requirements = reqs.readlines()
    return requirements


setup(
    name='gemini-solution-builder',
    version='1.0.0',
    description='Helps to create and build gemini solutions',
    long_description="""Helps to create and build gemini solutions""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Software Distribution"],
    author='GeminiOpenCloud',
    author_email='simon@geminiopencloud.com',
    url='http://geminiopencloud.com',
    keywords='Gemini solution',
    packages=find_packages(exclude=("examples",)),
    zip_safe=False,
    install_requires=find_requires(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gsb = gemini_solution_builder.cli:main',
            'gemini-solution-builder = gemini_solution_builder.cli:main']})
