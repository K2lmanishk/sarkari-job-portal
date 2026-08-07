from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.jobs.models import Job, Category, State
from apps.results.models import Result
from apps.admit_cards.models import AdmitCard
from apps.answer_keys.models import AnswerKey
from apps.syllabus.models import Syllabus
from apps.blog.models import Blog

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'core:privacy', 'core:disclaimer', 'core:terms',
                'jobs:job_list', 'results:result_list', 'admit_cards:admit_card_list',
                'answer_keys:answer_key_list', 'syllabus:syllabus_list', 'blog:blog_list']

    def location(self, item):
        return reverse(item)

class JobSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Job.objects.filter(is_active=True).only('slug', 'updated_at')

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('jobs:job_by_category', args=[obj.slug])

class StateSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return State.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('jobs:job_by_state', args=[obj.slug])

class ResultSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Result.objects.filter(is_active=True)

class AdmitCardSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return AdmitCard.objects.filter(is_active=True)

class AnswerKeySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return AnswerKey.objects.filter(is_active=True)

class SyllabusSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Syllabus.objects.all()

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.objects.filter(is_published=True)