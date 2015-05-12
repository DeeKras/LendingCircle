# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrowed_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_category', models.CharField(max_length=2, choices=[(b'AP', b'Apparel - clothing, shoes, accessories'), (b'JW', b'Jewelry'), (b'BK', b'Book'), (b'EL', b'Electronics'), (b'CD', b'CDs, DVDs'), (b'PG', b'Party Goods'), (b'TL', b'Tools'), (b'OT', b'other')])),
                ('item_short_desc', models.CharField(max_length=255)),
                ('item_detail_desc', models.TextField(blank=True)),
                ('expected_return_date', models.DateField(null=True, blank=True)),
                ('borrowed_condition', models.CharField(max_length=2, choices=[(b'NW', b'New'), (b'LN', b'Used, Like New'), (b'VG', b'Used, Very Good'), (b'GD', b'Used, Good'), (b'FR', b'Used, Fair'), (b'PR', b'Used, Poor')])),
                ('borrowed_comment', models.TextField(blank=True)),
                ('send_borrower_reminder', models.CharField(max_length=5, choices=[(b'Email', b'Email'), (b'Text', b'Text'), (b'None', b'None'), (b'Both', b'Both')])),
                ('borrowed_status', models.CharField(default=b'open', max_length=9, null=True, blank=True, choices=[(b'Open', b'Open: Still Borrowed'), (b'Returned', b'Returned'), (b'Forgiven', b"Forgiven: Don't expect to receive it back"), (b'Cancelled', b'Cancelled: Was never really lent after all')])),
                ('returned_date', models.DateField(null=True, blank=True)),
                ('returned_condition', models.CharField(blank=True, max_length=2, null=True, choices=[(b'NW', b'New'), (b'LN', b'Used, Like New'), (b'VG', b'Used, Very Good'), (b'GD', b'Used, Good'), (b'FR', b'Used, Fair'), (b'PR', b'Used, Poor')])),
                ('returned_comment', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BorrowTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('borrowed_date', models.DateTimeField(default=datetime.datetime(2015, 5, 12, 15, 26, 25, 391721, tzinfo=utc))),
                ('borrower', models.ForeignKey(related_name='borrower', to=settings.AUTH_USER_MODEL)),
                ('lender', models.ForeignKey(related_name='lender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initials', models.CharField(max_length=2, blank=True)),
                ('cell_phone', models.CharField(max_length=25)),
                ('location', models.CharField(max_length=50)),
                ('borrower_score', models.IntegerField(default=50)),
                ('lender_score', models.IntegerField(default=50)),
                ('items_lent', models.IntegerField(default=0)),
                ('items_borrowed', models.IntegerField(default=0)),
                ('items_returned', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='borrowed_item',
            name='borrow_transaction',
            field=models.ForeignKey(blank=True, to='lendborrow.BorrowTransaction', null=True),
            preserve_default=True,
        ),
    ]
