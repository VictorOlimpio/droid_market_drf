# Generated by Django 2.2.7 on 2019-11-27 01:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pieces', '0002_auto_20191127_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='piece',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
