from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Result

def result_list(request):
    results = Result.objects.filter(is_active=True).order_by('-result_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 20)
    try:
        results_paginated = paginator.page(page)
    except PageNotAnInteger:
        results_paginated = paginator.page(1)
    except EmptyPage:
        results_paginated = paginator.page(paginator.num_pages)
    return render(request, 'result_list.html', {
        'results': results_paginated,
        'page_obj': results_paginated
    })

def result_detail(request, slug):
    result = get_object_or_404(Result, slug=slug, is_active=True)
    result.views += 1
    result.save(update_fields=['views'])
    return render(request, 'result_detail.html', {'result': result})