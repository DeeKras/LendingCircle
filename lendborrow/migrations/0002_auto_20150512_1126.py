# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lendborrow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowtransaction',
            name='borrowed_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 12, 15, 26, 30, 239224, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
