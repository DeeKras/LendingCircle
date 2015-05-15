# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lendborrow', '0002_auto_20150512_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='items_borrowed_forgiven',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='items_lent_forgiven',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='items_lent_returned',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowed_item',
            name='borrowed_status',
            field=models.CharField(default=b'open', max_length=9, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowtransaction',
            name='borrowed_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 15, 2, 57, 57, 82907, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
