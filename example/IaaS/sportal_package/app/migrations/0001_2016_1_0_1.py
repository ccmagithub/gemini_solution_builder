# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('user_id', models.IntegerField(default=2)),
                ('is_show_flavor', models.BooleanField(default=True)),
                ('is_show_image', models.BooleanField(default=True)),
                ('is_show_network', models.BooleanField(default=True)),
                ('is_show_num_of_machines', models.BooleanField(default=True)),
                ('min_value_for_nom_choices', models.IntegerField(default=1)),
                ('max_value_for_nom_choices', models.IntegerField(default=1)),
                ('default_value_for_nom_choices',
                 models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('user_id', models.IntegerField(default=2)),
                ('is_show_flavor', models.BooleanField(default=True)),
                ('is_show_image', models.BooleanField(default=True)),
                ('is_show_public_ip', models.BooleanField(default=True)),
                ('is_show_private_ip', models.BooleanField(default=True)),
                ('is_show_machine_type', models.BooleanField(default=True)),
                ('is_show_remote_interface',
                 models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
