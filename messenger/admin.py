from django.contrib import admin
from .models import Message, ThreadManager, Thread

class MessageAdmin(admin.ModelAdmin):
    include = ('*')

class ThreadAdmin(admin.ModelAdmin):
    include = ('*')

admin.site.register(Message, MessageAdmin)

admin.site.register(Thread, ThreadAdmin)


