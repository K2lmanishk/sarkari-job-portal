from django.db import models
from django.utils.text import slugify

class Syllabus(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    organization = models.CharField(max_length=200)
    exam_name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    exam_pattern = models.TextField(blank=True, help_text="Detailed exam pattern")
    syllabus_content = models.TextField(blank=True, help_text="Full syllabus content")
    official_notification_url = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Syllabi"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title