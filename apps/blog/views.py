from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog, BlogCategory

def blog_list(request):
    posts = Blog.objects.filter(is_published=True).order_by('-published_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 12)
    try:
        posts_paginated = paginator.page(page)
    except PageNotAnInteger:
        posts_paginated = paginator.page(1)
    except EmptyPage:
        posts_paginated = paginator.page(paginator.num_pages)
    categories = BlogCategory.objects.all()
    return render(request, 'blog_list.html', {
        'posts': posts_paginated,
        'categories': categories,
        'page_obj': posts_paginated
    })

def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug, is_published=True)
    post.views += 1
    post.save(update_fields=['views'])
    related_posts = Blog.objects.filter(category=post.category).exclude(id=post.id)[:4]
    return render(request, 'blog_detail.html', {'post': post, 'related_posts': related_posts})

def blog_by_category(request, category_slug):
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = Blog.objects.filter(category=category, is_published=True)
    paginator = Paginator(posts, 12)
    page = request.GET.get('page', 1)
    try:
        posts_paginated = paginator.page(page)
    except PageNotAnInteger:
        posts_paginated = paginator.page(1)
    except EmptyPage:
        posts_paginated = paginator.page(paginator.num_pages)
    return render(request, 'blog_by_category.html', {
        'posts': posts_paginated,
        'category': category,
        'page_obj': posts_paginated
    })