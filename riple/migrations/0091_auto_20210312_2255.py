# Generated by Django 3.1.2 on 2021-03-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riple', '0090_auto_20210308_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]