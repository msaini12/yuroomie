# Generated by Django 2.0.2 on 2018-02-22 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20180221_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='creator_email',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='creator_phone',
            field=models.CharField(default='', max_length=14),
        ),
    ]
