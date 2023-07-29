from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from .models import Recipe, Category, Comment, Profile


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


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
