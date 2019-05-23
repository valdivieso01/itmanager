import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from private_storage.storage.files import PrivateFileSystemStorage
from simple_history.models import HistoricalRecords
from django.template.defaultfilters import slugify
from encrypted_model_fields.fields import EncryptedCharField
from ckeditor_uploader.fields import RichTextUploadingField
from private_storage.fields import PrivateFileField


storage1 = PrivateFileSystemStorage(
    location='/home/ubuntu/tesis/media/user-private/',
    base_url='/user-private/'
)


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    job = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['user__username']


# Uso señales para crear el perfil asociado al usuario automaticamente cuando se registra
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)


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


def upload_key(instance, filename):
    return os.path.join("%s/" % instance.profile.user, "keys/", filename)


class Key(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50)
    username = models.CharField(verbose_name="Username", max_length=50, blank=True, null=True)
    password = EncryptedCharField(verbose_name="Password", max_length=50, blank=True, null=True)
    note = models.CharField(verbose_name="Note", max_length=200, blank=True, null=True)
    url = models.CharField(verbose_name="URL", max_length=200, blank=True, null=True)
    file = PrivateFileField("File", storage=storage1, upload_to=upload_key, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Key"
        verbose_name_plural = "Keys"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Key, self).save(*args, **kwargs)


@receiver(post_save, sender=Key)
def save_key(sender, instance, **kwargs):

    if instance.file:
        input_file = instance.file.path
        output_file = instance.file.path
        with open(input_file, 'rb') as f:
            data = f.read()
        fernet = Fernet(settings.SECRET_KEY)
        encrypted = fernet.encrypt(data)
        with open(output_file, 'wb') as f:
            f.write(encrypted)


def upload_note(instance, filename):
    return os.path.join("%s/" % instance.profile.user, "notes/", filename)


class Note(CommonInfo):
    name = models.CharField(verbose_name="Name", max_length=50, unique=True)
    note = RichTextUploadingField(verbose_name="Text", blank=True, null=True)
    file = PrivateFileField("File", storage=storage1, upload_to=upload_note, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ['-last_modified_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Note, self).save(*args, **kwargs)


@receiver(post_save, sender=Note)
def save_note(sender, instance, **kwargs):
    if instance.file:
        input_file = instance.file.path
        output_file = instance.file.path

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(settings.SECRET_KEY)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

