# Generated by Django 2.0.2 on 2018-02-15 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20180214_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='thumbnail',
            field=models.FileField(default='https://content.thebrick.com/images/content/627064.jpg', upload_to=''),
            preserve_default=False,
        ),
    ]