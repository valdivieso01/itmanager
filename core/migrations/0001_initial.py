# Generated by Django 2.1.3 on 2018-11-19 02:17

import ckeditor_uploader.fields
import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import encrypted_model_fields.fields
import private_storage.fields
import private_storage.storage.files
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('note', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('file', private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(base_url='/media-private/', location='/home/javier/PycharmProjects/tesis/tesis/media/groups/'), upload_to=core.models.upload_backup, verbose_name='File')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_backup_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_backup_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Backup',
                'verbose_name_plural': 'Backups',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_group_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_group_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('guide', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Text')),
                ('file', private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(base_url='/media-private/', location='/home/javier/PycharmProjects/tesis/tesis/media/groups/'), upload_to=core.models.upload_guide, verbose_name='File')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_guide_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_guide_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Guide',
                'verbose_name_plural': 'Guides',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalKey',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Username')),
                ('password', encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True, verbose_name='Password')),
                ('note', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('file', models.TextField(blank=True, max_length=100, null=True, verbose_name='File')),
                ('slug', models.SlugField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Key',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Username')),
                ('password', encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True, verbose_name='Password')),
                ('note', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('file', private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(base_url='/media-private/', location='/home/javier/PycharmProjects/tesis/tesis/media/groups/'), upload_to=core.models.upload_key, verbose_name='File')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_key_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_key_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Key',
                'verbose_name_plural': 'Keys',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=100)),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_set_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Group')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_set_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Set',
                'verbose_name_plural': 'Sets',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('note', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('survey', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Text')),
                ('file', private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(base_url='/media-private/', location='/home/javier/PycharmProjects/tesis/tesis/media/groups/'), upload_to=core.models.upload_survey, verbose_name='File')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_survey_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_survey_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Set')),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('ip', models.IntegerField(blank=True, null=True, verbose_name='Ip')),
                ('connection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Connection')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Username')),
                ('password', models.CharField(blank=True, max_length=50, null=True, verbose_name='Password')),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Type')),
                ('observations', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveydevice_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveydevice_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Survey')),
            ],
            options={
                'verbose_name': 'Survey Server',
                'verbose_name_plural': 'Surveys Servers',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('number', models.CharField(max_length=50, verbose_name='Name')),
                ('responsable', models.CharField(blank=True, max_length=50, null=True, verbose_name='Responsable')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='Company')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Address')),
                ('telephone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telephone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('webpage', models.CharField(blank=True, max_length=50, null=True, verbose_name='Webpage')),
                ('person_incharge', models.CharField(blank=True, max_length=50, null=True, verbose_name='Person in charge')),
                ('workhours', models.CharField(blank=True, max_length=50, null=True, verbose_name='Workhours')),
                ('downtime', models.CharField(blank=True, max_length=50, null=True, verbose_name='Downtime')),
                ('business_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Business Name')),
                ('tax_residence', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tax Residence')),
                ('cuit', models.CharField(blank=True, max_length=50, null=True, verbose_name='CUIT')),
                ('category', models.CharField(blank=True, max_length=50, null=True, verbose_name='Category')),
                ('observations', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observation')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveygeneral_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveygeneral_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Survey')),
            ],
            options={
                'verbose_name': 'Survey General',
                'verbose_name_plural': 'Surveys Generals',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('ip', models.IntegerField(blank=True, null=True, verbose_name='Ip')),
                ('connection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Connection')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Username')),
                ('password', models.CharField(blank=True, max_length=50, null=True, verbose_name='Password')),
                ('services', models.CharField(blank=True, max_length=50, null=True, verbose_name='Services')),
                ('observations', models.TextField(blank=True, max_length=200, null=True, verbose_name='Note')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyserver_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyserver_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Survey')),
            ],
            options={
                'verbose_name': 'Survey Server',
                'verbose_name_plural': 'Surveys Servers',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('Department', models.CharField(blank=True, max_length=50, null=True, verbose_name='Department')),
                ('job_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Job Title')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone Number')),
                ('intern_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Intern Number')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='Country')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Address')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('observations', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observations')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyuser_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyuser_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Survey')),
            ],
            options={
                'verbose_name': 'Survey User',
                'verbose_name_plural': 'Surveys Users',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyWorkStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created_at')),
                ('last_modified_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='last_modified_at')),
                ('number', models.CharField(max_length=50, verbose_name='Name')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('charge', models.CharField(blank=True, max_length=50, null=True, verbose_name='Charge')),
                ('telephone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telephone')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('user_location', models.CharField(blank=True, max_length=50, null=True, verbose_name='User Location')),
                ('files_location', models.CharField(blank=True, max_length=50, null=True, verbose_name='Files Location')),
                ('windows_username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Windows Username')),
                ('windows_password', models.CharField(blank=True, max_length=50, null=True, verbose_name='Windows Password')),
                ('windows_version', models.CharField(blank=True, max_length=50, null=True, verbose_name='Windows Version')),
                ('software_additional', models.CharField(blank=True, max_length=50, null=True, verbose_name='Software Additional')),
                ('email_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Email Type')),
                ('server_connections', models.CharField(blank=True, max_length=50, null=True, verbose_name='Server Connections')),
                ('observations', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observation')),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyworkstation_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_surveyworkstation_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Survey')),
            ],
            options={
                'verbose_name': 'Survey WorkStation',
                'verbose_name_plural': 'Surveys WorkStations',
                'ordering': ['last_modified_at'],
            },
        ),
        migrations.AddField(
            model_name='key',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Set'),
        ),
        migrations.AddField(
            model_name='historicalkey',
            name='set',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Set'),
        ),
        migrations.AddField(
            model_name='guide',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Set'),
        ),
        migrations.AddField(
            model_name='backup',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Set'),
        ),
    ]
