from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'category', 'published_at', 'fetched_at']
    list_filter = ['category', 'source', 'published_at']
    search_fields = ['title', 'content', 'author']
    readonly_fields = ['fetched_at']

class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['favorite_categories', 'read_articles']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserPreferences, UserPreferencesAdmin)

