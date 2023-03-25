# from rest_framework.authtoken.admin import TokenAdmin
from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content_id',
        'user',
        'date_created',
        'body'
    ]

    list_filter = ('user', 'date_created', 'content_id')
