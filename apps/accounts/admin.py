from django.contrib import admin
from .models import UserProfile, SavedJob, JobAlert

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'preferred_state', 'preferred_category', 'qualification')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    date_hierarchy = 'saved_at'

@admin.register(JobAlert)
class JobAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'category', 'qualification', 'is_active', 'created_at')
    list_filter = ('is_active', 'state', 'category')