from django.contrib import admin
from .models import BlogCategory, Blog

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'published_at', 'views')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ('views',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'featured_image', 'excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'keywords')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at', 'views')
        }),
    )