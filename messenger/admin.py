from django.contrib import admin
from .models import Message, ThreadManager, Thread

class MessageAdmin(admin.ModelAdmin):
    exclude = ('')

class ThreadAdmin(admin.ModelAdmin):
    exclude = ('')

admin.site.register(Message, MessageAdmin)

admin.site.register(Thread, ThreadAdmin)


