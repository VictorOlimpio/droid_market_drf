# Generated by Django 2.2.7 on 2019-11-28 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0002_auto_20191127_1741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demand',
            old_name='cep',
            new_name='postal_code',
        ),
    ]
