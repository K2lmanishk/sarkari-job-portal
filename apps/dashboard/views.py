from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from apps.jobs.models import Job, Category, State
from apps.results.models import Result
from apps.admit_cards.models import AdmitCard
from apps.answer_keys.models import AnswerKey
from apps.syllabus.models import Syllabus
from apps.blog.models import Blog
from apps.core.models import Contact

@staff_member_required
def dashboard_home(request):
    today = timezone.now().date()

    context = {
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'expired_jobs': Job.objects.filter(application_last_date__lt=today).count(),
        'upcoming_jobs': Job.objects.filter(application_start_date__gt=today, is_active=True).count(),
        'total_results': Result.objects.count(),
        'total_admit_cards': AdmitCard.objects.count(),
        'total_answer_keys': AnswerKey.objects.count(),
        'total_blog_posts': Blog.objects.count(),
        'total_contacts': Contact.objects.count(),
        'total_categories': Category.objects.count(),
        'total_states': State.objects.count(),
        'total_syllabus': Syllabus.objects.count(),
    }
    return render(request, 'dashboard/index.html', context)