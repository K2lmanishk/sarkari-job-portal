from django.db import models
from django.db import OperationalError


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class SiteSettings(models.Model):
    """Singleton model for homepage SEO and global settings."""
    homepage_title = models.CharField(max_length=200, default="Latest Government Jobs 2026 | Sarkari Job Portal")
    homepage_meta_description = models.TextField(default="Get latest government jobs, Sarkari Naukri, results, admit cards, answer keys, syllabus and exam updates.")
    about_us = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    telegram_link = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            obj, created = cls.objects.get_or_create(pk=1)
            return obj
        except OperationalError:
            # Table hasn't been created yet – return an in-memory dummy
            return cls(
                pk=1,
                homepage_title="Latest Government Jobs 2026 | Sarkari Job Portal",
                homepage_meta_description="Get latest government jobs, Sarkari Naukri, results, admit cards, answer keys, syllabus and exam updates.",
            )