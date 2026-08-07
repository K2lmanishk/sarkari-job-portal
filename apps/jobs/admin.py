from django.contrib import admin
from .models import Category, State, Job, FAQ

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 0
    fields = ('question', 'answer', 'order', 'is_active')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'state', 'category', 'total_vacancies',
                    'application_last_date', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'category', 'state', 'qualification')
    search_fields = ('title', 'organization', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [FAQInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'organization', 'short_description', 'description', 'category', 'state', 'district')
        }),
        ('Vacancy Details', {
            'fields': ('total_vacancies', 'qualification', 'age_min', 'age_max', 'age_relaxation', 'salary', 'job_location')
        }),
        ('Dates', {
            'fields': ('application_start_date', 'application_last_date', 'exam_date', 'admit_card_date')
        }),
        ('Fees', {
            'fields': ('application_fee_general', 'application_fee_obc', 'application_fee_sc', 'application_fee_st', 'application_fee_female')
        }),
        ('Process & Instructions', {
            'fields': ('selection_process', 'eligibility', 'how_to_apply', 'important_instructions')
        }),
        ('Official Links', {
            'fields': ('official_notification_url', 'official_apply_url', 'official_website_url')
        }),
        ('Status & Visibility', {
            'fields': ('featured', 'is_active', 'status', 'views')
        }),
    )
    readonly_fields = ('views',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'job', 'order', 'is_active')
    list_filter = ('job',)