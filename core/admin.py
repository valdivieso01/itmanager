from django.contrib import admin
from .models import Group, Set, Key, Backup, Survey, Guide


class GroupAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class SetAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class KeyAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class GuideAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class BackupAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


class SurveyAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'last_modified_at', 'created_by', 'last_modified_by', 'slug')


admin.site.register(Group, GroupAdmin)

admin.site.register(Set, SetAdmin)

admin.site.register(Key, KeyAdmin)

admin.site.register(Guide, GuideAdmin)

admin.site.register(Backup, BackupAdmin)

admin.site.register(Survey, SurveyAdmin)