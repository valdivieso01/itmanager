# Generated by Django 2.1.3 on 2019-02-04 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190204_0510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='qr',
        ),
    ]
