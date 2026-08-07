from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class or icon name")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Job(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('apply_now', 'Apply Now'),
        ('closing_soon', 'Closing Soon'),
        ('closed', 'Application Closed'),
        ('exam_soon', 'Exam Soon'),
        ('result_declared', 'Result Declared'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    organization = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    district = models.CharField(max_length=100, blank=True)

    total_vacancies = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=200, blank=True)   # e.g., "10th Pass, 12th Pass"
    age_min = models.PositiveIntegerField(null=True, blank=True)
    age_max = models.PositiveIntegerField(null=True, blank=True)
    age_relaxation = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=200, blank=True)
    job_location = models.CharField(max_length=200, blank=True)

    application_start_date = models.DateField(null=True, blank=True)
    application_last_date = models.DateField(null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    admit_card_date = models.DateField(null=True, blank=True)

    application_fee_general = models.CharField(max_length=50, blank=True)
    application_fee_obc = models.CharField(max_length=50, blank=True)
    application_fee_sc = models.CharField(max_length=50, blank=True)
    application_fee_st = models.CharField(max_length=50, blank=True)
    application_fee_female = models.CharField(max_length=50, blank=True)

    selection_process = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    how_to_apply = models.TextField(blank=True)
    important_instructions = models.TextField(blank=True)

    official_notification_url = models.URLField(max_length=500, blank=True)
    official_apply_url = models.URLField(max_length=500, blank=True)
    official_website_url = models.URLField(max_length=500, blank=True)

    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto‑update status based on dates (can be overridden manually)
        today = timezone.now().date()
        if self.application_last_date and self.application_last_date < today:
            self.status = 'closed'
        elif self.application_last_date and (self.application_last_date - today).days <= 3:
            if self.status != 'closed':
                self.status = 'closing_soon'
        # Add more logic as needed; manual override remains possible
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return f"{self.job.title} - {self.question[:50]}"