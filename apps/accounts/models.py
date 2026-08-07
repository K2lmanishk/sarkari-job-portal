from django.db import models
from django.contrib.auth.models import User
from apps.jobs.models import Job, Category, State

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    preferred_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')   # prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"

class JobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_alerts')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user.username}"