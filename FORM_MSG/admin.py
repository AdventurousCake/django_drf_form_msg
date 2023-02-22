from django.contrib import admin

# Register your models here.
from .models import Message, Like, Comment

admin.site.register(Message)
admin.site.register(Like)
admin.site.register(Comment)
