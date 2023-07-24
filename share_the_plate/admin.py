from django.contrib import admin
from .models import Recipe, Category, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_at')
    list_display = ('title', 'slug', 'status', 'created_at')
    search_fields = ['title', 'ingredients']
    summernote_fields = ('ingredients', 'instructions')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('body', 'user', 'created_at', 'recipe')
    list_filter = ('created_at', 'user')
    search_fields = ['body', 'email', 'user']

    name = Comment.user

