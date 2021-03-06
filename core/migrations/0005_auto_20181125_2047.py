# Generated by Django 2.1.3 on 2018-11-25 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20181124_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyworkstation',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='surveyworkstation',
            name='last_name',
        ),
        migrations.AddField(
            model_name='surveyworkstation',
            name='user',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='surveyuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Full Name'),
        ),
    ]
