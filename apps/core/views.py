from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact, NewsletterSubscription, SiteSettings
from apps.jobs.models import Job, Category, State
from apps.results.models import Result
from apps.admit_cards.models import AdmitCard
from apps.answer_keys.models import AnswerKey
from apps.blog.models import Blog
from django.db.models import Count

def home(request):
    settings = SiteSettings.load()
    latest_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:10]
    latest_results = Result.objects.filter(is_active=True).order_by('-result_date')[:6]
    latest_admit_cards = AdmitCard.objects.filter(is_active=True).order_by('-release_date')[:6]
    latest_answer_keys = AnswerKey.objects.filter(is_active=True).order_by('-release_date')[:6]
    categories = Category.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    blog_posts = Blog.objects.filter(is_published=True).order_by('-published_at')[:4]

    qualifications = [
        "10th Pass", "12th Pass", "ITI", "Diploma",
        "Graduation", "Post Graduation", "BCA", "BTech"
    ]

    # Hero stats
    total_active_jobs = Job.objects.filter(is_active=True).count()
    total_results = Result.objects.filter(is_active=True).count()
    total_admit_cards = AdmitCard.objects.filter(is_active=True).count()

    context = {
        'settings': settings,
        'latest_jobs': latest_jobs,
        'latest_results': latest_results,
        'latest_admit_cards': latest_admit_cards,
        'latest_answer_keys': latest_answer_keys,
        'categories': categories,
        'states': states,
        'blog_posts': blog_posts,
        'qualifications': qualifications,
        'total_active_jobs': total_active_jobs,
        'total_results': total_results,
        'total_admit_cards': total_admit_cards,
    }
    return render(request, 'home.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def about(request):
    settings = SiteSettings.load()
    return render(request, 'about.html', {'settings': settings})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'Your message has been sent. We will get back to you soon.')
        return redirect('core:contact')
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')

def terms(request):
    return render(request, 'terms.html')

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscription.objects.get_or_create(email=email)
            messages.success(request, 'Subscribed successfully!')
        return redirect('core:home')
    return redirect('core:home')