# Generated by Django 3.1.2 on 2021-03-06 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riple', '0079_auto_20210306_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='files/'),
        ),
    ]