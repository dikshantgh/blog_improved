# Generated by Django 3.0 on 2020-03-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200325_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'get_latest_by': 'publish'},
        ),
    ]
