# Generated by Django 3.0 on 2020-03-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200326_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]