from django.contrib import admin
from .models import AnswerKey

@admin.register(AnswerKey)
class AnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'exam_name', 'release_date', 'is_active', 'views')
    list_filter = ('is_active', 'organization')
    search_fields = ('title', 'exam_name', 'organization')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'release_date'
    readonly_fields = ('views',)