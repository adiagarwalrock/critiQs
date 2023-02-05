from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'content_id',
        'user',
        'date_created',
        'body'
    ]
