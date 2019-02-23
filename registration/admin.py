from django.contrib import admin
from .models import Key, Note, Profile


class KeyAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class NoteAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class ProfileAdmin(admin.ModelAdmin):
    exclude = ('',)


admin.site.register(Key, KeyAdmin)

admin.site.register(Note, NoteAdmin)

admin.site.register(Profile, ProfileAdmin)