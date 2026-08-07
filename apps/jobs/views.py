from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Job, Category, State

def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('category', 'state')

    # Filtering
    state = request.GET.get('state')
    category = request.GET.get('category')
    qualification = request.GET.get('qualification')
    job_type = request.GET.get('job_type')  # e.g., 'upcoming', 'closing_soon'
        # Sorting
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['-created_at', 'created_at', '-application_last_date', 'application_last_date',
                     '-total_vacancies', 'total_vacancies', 'title', '-title']
    if sort not in allowed_sorts:
        sort = '-created_at'
    jobs = jobs.order_by(sort)
    organization = request.GET.get('organization')
    search = request.GET.get('q')

    if state:
        jobs = jobs.filter(state__slug=state)
    if category:
        jobs = jobs.filter(category__slug=category)
    if qualification:
        jobs = jobs.filter(qualification__icontains=qualification)
    if job_type:
        today = timezone.now().date()
        if job_type == 'upcoming':
            jobs = jobs.filter(application_start_date__gt=today)
        elif job_type == 'closing_soon':
            jobs = jobs.filter(application_last_date__gte=today,
                               application_last_date__lte=today + timezone.timedelta(days=3))
        elif job_type == 'closed':
            jobs = jobs.filter(application_last_date__lt=today)
        elif job_type == 'exam_soon':
            jobs = jobs.filter(exam_date__gte=today)
    if organization:
        jobs = jobs.filter(organization__icontains=organization)
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(organization__icontains=search) |
            Q(short_description__icontains=search) |
            Q(qualification__icontains=search)
        )

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(jobs, 20)
    try:
        jobs_paginated = paginator.page(page)
    except PageNotAnInteger:
        jobs_paginated = paginator.page(1)
    except EmptyPage:
        jobs_paginated = paginator.page(paginator.num_pages)

    # Get filter options
    categories = Category.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)

    context = {
        'jobs': jobs_paginated,
        'categories': categories,
        'states': states,
        'request_params': request.GET.copy(),
    }
    return render(request, 'job_list.html', context)

def job_search(request):
    # Redirect to job_list with search query
    query = request.GET.get('q', '')
    return redirect(f'/jobs/?q={query}')

def job_detail(request, slug):
    job = get_object_or_404(Job.objects.select_related('category', 'state'), slug=slug, is_active=True)
    # Increment views (simple approach)
    job.views += 1
    job.save(update_fields=['views'])
    # Related jobs
    related_jobs = Job.objects.filter(
        Q(category=job.category) | Q(state=job.state) | Q(organization=job.organization)
    ).exclude(id=job.id).filter(is_active=True).order_by('-created_at')[:6]
    context = {'job': job, 'related_jobs': related_jobs}
    return render(request, 'job_detail.html', context)

def job_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    jobs = Job.objects.filter(category=category, is_active=True)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page', 1)
    try:
        jobs_paginated = paginator.page(page)
    except PageNotAnInteger:
        jobs_paginated = paginator.page(1)
    except EmptyPage:
        jobs_paginated = paginator.page(paginator.num_pages)
        context = {'jobs': jobs_paginated, 'category': category, 'page_obj': jobs_paginated}
        return render(request, 'job_by_category.html', context)
    
    
def job_by_state(request, state_slug):
    state = get_object_or_404(State, slug=state_slug)
    jobs = Job.objects.filter(state=state, is_active=True)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page', 1)
    try:
        jobs_paginated = paginator.page(page)
    except PageNotAnInteger:
        jobs_paginated = paginator.page(1)
    except EmptyPage:
        jobs_paginated = paginator.page(paginator.num_pages)
    context = {'jobs': jobs_paginated, 'state': state}
    return render(request, 'job_by_state.html', context)

def job_by_qualification(request, qualification):
    jobs = Job.objects.filter(qualification__icontains=qualification, is_active=True)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page', 1)
    try:
        jobs_paginated = paginator.page(page)
    except PageNotAnInteger:
        jobs_paginated = paginator.page(1)
    except EmptyPage:
        jobs_paginated = paginator.page(paginator.num_pages)
    context = {'jobs': jobs_paginated, 'qualification': qualification}
    return render(request, 'job_by_qualification.html', context)

# Need to import timezone and redirect for job_search
from django.utils import timezone
from django.shortcuts import redirect