import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from encrypted_model_fields.fields import EncryptedCharField
from ckeditor_uploader.fields import RichTextUploadingField
from private_storage.fields import PrivateFileField
from private_storage.storage.files import PrivateFileSystemStorage
from simple_history.models import HistoricalRecords

import os, random, struct
from Crypto.Cipher import AES
import hashlib

def encrypt_file(key, in_filename, out_filename, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))



storage2 = PrivateFileSystemStorage(
    location='/home/ubuntu/tesis/media/groups/',
    base_url='/group-private/'
)


class CommonInfo(models.Model):
    created_at = models.DateTimeField("created_at", default=now, blank=True)
    last_modified_at = models.DateTimeField("last_modified_at", default=now, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Created by",
                                   related_name="%(app_label)s_%(class)s_created", on_delete=models.CASCADE, null=True,
                                   blank=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Last modified by",
                                         related_name="%(app_label)s_%(class)s_last_modified", on_delete=models.CASCADE,
                                         null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now()

        self.last_modified_at = now()
        super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Group(CommonInfo):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(User)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)


class Set(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    description = models.CharField(max_length=100, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Set"
        verbose_name_plural = "Sets"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Set, self).save(*args, **kwargs)


def upload_key(instance, filename):
    return os.path.join("%s/" % instance.set.group.pk, "keys/", filename)


class Key(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    username = models.CharField(verbose_name="Username", max_length=50, blank=True, null=True)
    password = EncryptedCharField(verbose_name="Password", max_length=50, blank=True, null=True)
    note = models.CharField(verbose_name="Note", max_length=200, blank=True, null=True)
    url = models.CharField(verbose_name="URL", max_length=50, blank=True, null=True)
    file = PrivateFileField("File", storage=storage2, upload_to=upload_key, blank=True, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    slug = models.SlugField()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Key"
        verbose_name_plural = "Keys"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        password = 'kitty'
        key = hashlib.sha256(password.encode('utf-8')).digest()
        self.file = encrypt_file(key, self.file, self.file, chunksize=64*1024)
        super(Key, self).save(*args, **kwargs)

def upload_guide(instance, filename):
    return os.path.join("%s/" % instance.set.group.pk, "guides/", filename)


class Guide(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    guide = RichTextUploadingField(verbose_name="Text", blank=True, null=True)
    file = PrivateFileField("File", storage=storage2, upload_to=upload_guide, blank=True, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Guide"
        verbose_name_plural = "Guides"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Guide, self).save(*args, **kwargs)


def upload_backup(instance, filename):
    return os.path.join("%s/" % instance.set.group.pk, "backups/", filename)


class Backup(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    note = models.CharField(verbose_name="Note", max_length=200, blank=True, null=True)
    file = PrivateFileField("File", storage=storage2, upload_to=upload_backup)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Backup"
        verbose_name_plural = "Backups"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Backup, self).save(*args, **kwargs)


def upload_survey(instance, filename):
    return os.path.join("%s/" % instance.set.group.pk, "surveys/", filename)


class Survey(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    responsable = models.CharField(verbose_name="Responsable", max_length=50, blank=True, null=True)
    company = models.CharField(verbose_name="Company", max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name="Address", max_length=50, blank=True, null=True)
    telephone = models.CharField(verbose_name="Telephone", max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=50, blank=True, null=True)
    webpage = models.CharField(verbose_name="Webpage", max_length=50, blank=True, null=True)
    person_incharge = models.CharField(verbose_name="Person in charge", max_length=50, blank=True, null=True)
    workhours = models.CharField(verbose_name="Workhours", max_length=50, blank=True, null=True)
    downtime = models.CharField(verbose_name="Downtime", max_length=50, blank=True, null=True)
    business_name = models.CharField(verbose_name="Business Name", max_length=50, blank=True, null=True)
    tax_residence = models.CharField(verbose_name="Tax Residence", max_length=50, blank=True, null=True)
    cuit = models.CharField(verbose_name="CUIT", max_length=50, blank=True, null=True)
    category = models.CharField(verbose_name="Category", max_length=50, blank=True, null=True)
    observations = models.TextField(verbose_name="Observation", max_length=200, blank=True, null=True)
    file = PrivateFileField("File", storage=storage2, upload_to=upload_backup, blank=True, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Survey, self).save(*args, **kwargs)


class SurveyWorkStation(CommonInfo):
    number = models.CharField(verbose_name="Number", max_length=50)
    user = models.CharField(verbose_name="User", max_length=50, blank=True, null=True)
    charge = models.CharField(verbose_name="Charge", max_length=50, blank=True, null=True)
    telephone = models.CharField(verbose_name="Telephone", max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=50, blank=True, null=True)
    user_location = models.CharField(verbose_name="User Location", max_length=50, blank=True, null=True)
    files_location = models.CharField(verbose_name="Files Location", max_length=50, blank=True, null=True)
    windows_username = models.CharField(verbose_name="Windows Username", max_length=50, blank=True, null=True)
    windows_password = models.CharField(verbose_name="Windows Password", max_length=50, blank=True, null=True)
    windows_version = models.CharField(verbose_name="Windows Version", max_length=50, blank=True, null=True)
    software_additional = models.CharField(verbose_name="Software Additional", max_length=50, blank=True, null=True)
    email_type = models.CharField(verbose_name="Email Type", max_length=50, blank=True, null=True)
    server_connections = models.CharField(verbose_name="Server Connections", max_length=50, blank=True, null=True)
    observations = models.TextField(verbose_name="Observation", max_length=200, blank=True, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Survey WorkStation"
        verbose_name_plural = "Surveys WorkStations"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.slug = slugify(self.number)
        super(SurveyWorkStation, self).save(*args, **kwargs)


class SurveyUser(CommonInfo):
    full_name = models.CharField(verbose_name="Full Name", max_length=50, blank=True, null=True)
    Department = models.CharField(verbose_name="Department", max_length=50, blank=True, null=True)
    job_title = models.CharField(verbose_name="Job Title", max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=50, blank=True, null=True)
    intern_number = models.CharField(verbose_name="Intern Number", max_length=50, blank=True, null=True)
    country = models.CharField(verbose_name="Country", max_length=50, blank=True, null=True)
    city = models.CharField(verbose_name="City", max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name="Address", max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=50, blank=True, null=True)
    observations = models.TextField(verbose_name="Observations", max_length=200, blank=True, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Survey User"
        verbose_name_plural = "Surveys Users"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(SurveyUser, self).save(*args, **kwargs)


class SurveyServer(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50, blank=True, null=True)
    ip = models.IntegerField(verbose_name="Ip", blank=True, null=True)
    connection = models.CharField(verbose_name="Connection", max_length=50, blank=True, null=True)
    username = models.CharField(verbose_name="Username", max_length=50, blank=True, null=True)
    password = models.CharField(verbose_name="Password", max_length=50, blank=True, null=True)
    services = models.CharField(verbose_name="Services", max_length=50, blank=True, null=True)
    observations = models.TextField(verbose_name="Note", max_length=200, blank=True, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Survey Server"
        verbose_name_plural = "Surveys Servers"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SurveyServer, self).save(*args, **kwargs)


class SurveyDevice(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50, blank=True, null=True)
    ip = models.IntegerField(verbose_name="Ip", blank=True, null=True)
    connection = models.CharField(verbose_name="Connection", max_length=50, blank=True, null=True)
    username = models.CharField(verbose_name="Username", max_length=50, blank=True, null=True)
    password = models.CharField(verbose_name="Password", max_length=50, blank=True, null=True)
    type = models.CharField(verbose_name="Type", max_length=50, blank=True, null=True)
    observations = models.TextField(verbose_name="Note", max_length=200, blank=True, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Survey Server"
        verbose_name_plural = "Surveys Servers"
        ordering = ['last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SurveyDevice, self).save(*args, **kwargs)
