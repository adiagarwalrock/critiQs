# from rest_framework.authtoken.admin import TokenAdmin
from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'body',
        'content_id',
        'date_created',
        'user',
    ]

    list_filter = ('user', 'date_created', 'content_id')
