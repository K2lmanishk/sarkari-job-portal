from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import AnswerKey

def answer_key_list(request):
    answer_keys = AnswerKey.objects.filter(is_active=True).order_by('-release_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(answer_keys, 20)
    try:
        answer_keys_paginated = paginator.page(page)
    except PageNotAnInteger:
        answer_keys_paginated = paginator.page(1)
    except EmptyPage:
        answer_keys_paginated = paginator.page(paginator.num_pages)
    return render(request, 'answer_key_list.html', {
        'answer_keys': answer_keys_paginated,
        'page_obj': answer_keys_paginated
    })

def answer_key_detail(request, slug):
    answer_key = get_object_or_404(AnswerKey, slug=slug, is_active=True)
    answer_key.views += 1
    answer_key.save(update_fields=['views'])
    return render(request, 'answer_key_detail.html', {'answer_key': answer_key})