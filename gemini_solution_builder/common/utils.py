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


import os
import prettytable


class Model(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars.

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def print_list(objs, fields, formatters={}, order_by=None):
    pt = prettytable.PrettyTable([f for f in fields],
                                 caching=False, print_empty=False)
    pt.aligns = ['l' for f in fields]

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                field_name = field.lower().replace(' ', '_')
                data = getattr(o, field_name, '')
                # data = o.get(field_name, '')
                if data is None:
                    data = ''
                row.append(data)
        pt.add_row(row)

    if order_by is None:
        order_by = fields[0]
    print(pt.get_string(sortby=order_by))
