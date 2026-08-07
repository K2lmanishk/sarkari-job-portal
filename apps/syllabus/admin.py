from django.contrib import admin
from .models import Syllabus

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'exam_name', 'created_at')
    search_fields = ('title', 'exam_name', 'organization')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'