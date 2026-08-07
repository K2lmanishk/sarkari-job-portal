from django.db import models
from django.utils.text import slugify

class AnswerKey(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    organization = models.CharField(max_length=200)
    exam_name = models.CharField(max_length=300)
    release_date = models.DateField()
    description = models.TextField(blank=True)
    answer_key_url = models.URLField(max_length=500, blank=True, help_text="Direct link to answer key")
    official_website_url = models.URLField(max_length=500, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-release_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title