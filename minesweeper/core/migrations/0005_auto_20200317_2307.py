# Generated by Django 3.0.4 on 2020-03-17 23:07

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200317_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboard',
            name='plays',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
    ]
