from django.contrib import admin
from Issues.models import Issues, Comments


@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_open')
    list_filter = ['is_open']
    search_fields = ['name']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
