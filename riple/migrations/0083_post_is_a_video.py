# Generated by Django 3.1.2 on 2021-03-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riple', '0082_auto_20210306_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_a_video',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]