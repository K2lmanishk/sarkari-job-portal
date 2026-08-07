from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import AdmitCard

def admit_card_list(request):
    admit_cards = AdmitCard.objects.filter(is_active=True).order_by('-release_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(admit_cards, 20)
    try:
        admit_cards_paginated = paginator.page(page)
    except PageNotAnInteger:
        admit_cards_paginated = paginator.page(1)
    except EmptyPage:
        admit_cards_paginated = paginator.page(paginator.num_pages)
    return render(request, 'admit_card_list.html', {
        'admit_cards': admit_cards_paginated,
        'page_obj': admit_cards_paginated
    })

def admit_card_detail(request, slug):
    admit_card = get_object_or_404(AdmitCard, slug=slug, is_active=True)
    admit_card.views += 1
    admit_card.save(update_fields=['views'])
    return render(request, 'admit_card_detail.html', {'admit_card': admit_card})