# Generated by Django 2.0.2 on 2018-02-16 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20180216_0019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='visists',
            new_name='visits',
        ),
    ]