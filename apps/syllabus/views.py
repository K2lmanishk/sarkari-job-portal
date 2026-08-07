from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Syllabus

def syllabus_list(request):
    syllabi = Syllabus.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(syllabi, 20)
    try:
        syllabi_paginated = paginator.page(page)
    except PageNotAnInteger:
        syllabi_paginated = paginator.page(1)
    except EmptyPage:
        syllabi_paginated = paginator.page(paginator.num_pages)
    return render(request, 'syllabus_list.html', {
        'syllabi': syllabi_paginated,
        'page_obj': syllabi_paginated
    })

def syllabus_detail(request, slug):
    syllabus = get_object_or_404(Syllabus, slug=slug)
    return render(request, 'syllabus_detail.html', {'syllabus': syllabus})