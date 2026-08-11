from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from .models import Job, Category, State


def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('category', 'state')

    # Filtering
    state = request.GET.get('state')
    category = request.GET.get('category')
    qualification = request.GET.get('qualification')
    job_type = request.GET.get('job_type')  # 'upcoming', 'closing_soon', etc.
    organization = request.GET.get('organization')
    search = request.GET.get('q')

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['-created_at', 'created_at', '-application_last_date', 'application_last_date',
                     '-total_vacancies', 'total_vacancies', 'title', '-title']
    if sort not in allowed_sorts:
        sort = '-created_at'
    jobs = jobs.order_by(sort)

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

    # Filter options for dropdowns
    categories = Category.objects.filter(is_active=True)
    states = State.objects.filter(is_active=True)
    qualifications = (
        Job.objects.filter(is_active=True)
        .values_list('qualification', flat=True)
        .distinct()
        .order_by('qualification')
    )
    organizations = (
        Job.objects.filter(is_active=True)
        .values_list('organization', flat=True)
        .distinct()
        .order_by('organization')
    )

    context = {
        'jobs': jobs_paginated,
        'categories': categories,
        'states': states,
        'qualifications': qualifications,
        'organizations': organizations,
        'request_params': request.GET.copy(),
    }
    return render(request, 'job_list.html', context)


def job_search(request):
    query = request.GET.get('q', '')
    return redirect(f'/jobs/?q={query}')


def job_detail(request, slug):
    job = get_object_or_404(
        Job.objects.select_related('category', 'state'),
        slug=slug,
        is_active=True
    )
    # Increment view count
    job.views += 1
    job.save(update_fields=['views'])

    # --- Related jobs logic ---
    # Priority: same category, then same state, then same organization
    related_qs = Job.objects.filter(
        Q(category=job.category) |
        Q(state=job.state) |
        Q(organization=job.organization)
    ).exclude(id=job.id).filter(is_active=True).order_by('-created_at')[:8]

    # If not enough related jobs, fill with latest active jobs
    if related_qs.count() < 6:
        fallback_qs = Job.objects.filter(is_active=True).exclude(
            id__in=[job.id] + list(related_qs.values_list('id', flat=True))
        ).order_by('-created_at')[:6]
        related_jobs = list(related_qs) + list(fallback_qs)
        related_jobs = related_jobs[:8]   # keep total at 8
    else:
        related_jobs = related_qs

    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    return render(request, 'job_detail.html', context)


def job_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    jobs = Job.objects.filter(category=category, is_active=True).order_by('-created_at')
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
    jobs = Job.objects.filter(state=state, is_active=True).order_by('-created_at')
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
    jobs = Job.objects.filter(qualification__icontains=qualification, is_active=True).order_by('-created_at')
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