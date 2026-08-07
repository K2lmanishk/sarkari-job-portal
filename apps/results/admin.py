from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'exam_name', 'result_date', 'is_active', 'views')
    list_filter = ('is_active', 'organization', 'result_date')
    search_fields = ('title', 'exam_name', 'organization')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'result_date'
    readonly_fields = ('views',)