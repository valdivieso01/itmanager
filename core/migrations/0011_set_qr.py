# Generated by Django 2.1.3 on 2019-02-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190102_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='qr',
            field=models.CharField(default='http://itmanager.site/qr_search/1', max_length=50, verbose_name='QR'),
        ),
    ]
