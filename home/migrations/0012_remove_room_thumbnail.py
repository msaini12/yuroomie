# Generated by Django 2.0.2 on 2018-02-16 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20180216_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='thumbnail',
        ),
    ]