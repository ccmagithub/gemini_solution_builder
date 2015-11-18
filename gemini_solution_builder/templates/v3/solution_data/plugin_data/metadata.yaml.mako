# Solution name
name: ${solution_name}
# Human-readable name for your solution
title: Title for ${solution_name} solution
# Solution version
version: '1.0.0'
# Description
description: Enable to use solution X for Neutron
# Required gemini version
gemini_version: ['7.0', '8.0']
# Specify license of your solution
licenses: ['Apache License Version 2.0']
# Specify author or company name
authors: ['Specify author or company name']
# A link to the solution's page
homepage: 'https://github.com/stackforge/gemini-solutions'
# Specify a group which your solution implements, possible options:
# network, storage, storage::cinder, storage::glance, hypervisor
groups: []

# The solution is compatible with releases in the list
releases:
  - os: ubuntu
    version: 2015.1.0-7.0
    mode: ['ha']
    deployment_scripts_path: deployment_scripts/
    repository_path: repositories/ubuntu
  - os: ubuntu
    version: 2015.1.0-8.0
    mode: ['ha']
    deployment_scripts_path: deployment_scripts/
    repository_path: repositories/ubuntu

# Version of solution package
package_version: '3.0.0'
