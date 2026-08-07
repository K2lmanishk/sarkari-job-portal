from django.contrib import admin
from .models import Contact, NewsletterSubscription, SiteSettings

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)

@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Only one instance allowed – hide add button
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    fields = ('homepage_title', 'homepage_meta_description', 'about_us', 'contact_email', 'telegram_link', 'whatsapp_link')