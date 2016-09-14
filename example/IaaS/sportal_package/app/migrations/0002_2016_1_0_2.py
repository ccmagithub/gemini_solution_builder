# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


CREATESITE = [
    {
        'is_show_flavor': True,
        'is_show_image': True,
        'is_show_network': False,
        'is_show_num_of_machines': True,
        'min_value_for_nom_choices': 1,
        'max_value_for_nom_choices': 2,
        'default_value_for_nom_choices': 1
    }
]


SITEDETAIL = [
    {
        'is_show_flavor': True,
        'is_show_image': True,
        'is_show_public_ip': True,
        'is_show_private_ip': True,
        'is_show_machine_type': True,
        'is_show_remote_interface': True
    }
]


def gen_init_data(apps, schema_editor):
    CreateSite = apps.get_model('iaas', 'CreateSite')
    for cs in CREATESITE:
        cs_obj = CreateSite(
            is_show_flavor=cs['is_show_flavor'],
            is_show_image=cs['is_show_image'],
            is_show_network=cs['is_show_network'],
            is_show_num_of_machines=cs['is_show_num_of_machines'],
            min_value_for_nom_choices=cs['min_value_for_nom_choices'],
            max_value_for_nom_choices=cs['max_value_for_nom_choices'],
            default_value_for_nom_choices=cs['default_value_for_nom_choices'])
        cs_obj.save()

    SiteDetail = apps.get_model('iaas', 'SiteDetail')
    for sd in SITEDETAIL:
        sd_obj = SiteDetail(
            is_show_flavor=sd['is_show_flavor'],
            is_show_image=sd['is_show_image'],
            is_show_public_ip=sd['is_show_public_ip'],
            is_show_private_ip=sd['is_show_private_ip'],
            is_show_machine_type=sd['is_show_machine_type'],
            is_show_remote_interface=sd['is_show_remote_interface'])
        sd_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('iaas', '0001_2016_1_0_1'),
    ]

    operations = [
        migrations.RunPython(gen_init_data)
    ]
