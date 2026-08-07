from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import (
    StaticViewSitemap, JobSitemap, CategorySitemap, StateSitemap,
    ResultSitemap, AdmitCardSitemap, AnswerKeySitemap, SyllabusSitemap, BlogSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'jobs': JobSitemap,
    'categories': CategorySitemap,
    'states': StateSitemap,
    'results': ResultSitemap,
    'admit_cards': AdmitCardSitemap,
    'answer_keys': AnswerKeySitemap,
    'syllabus': SyllabusSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Core pages (home, about, contact, etc.)
    path('', include('apps.core.urls', namespace='core')),

    # Jobs
    path('jobs/', include('apps.jobs.urls', namespace='jobs')),

    # Results
    path('results/', include('apps.results.urls', namespace='results')),

    # Admit Cards
    path('admit-card/', include('apps.admit_cards.urls', namespace='admit_cards')),

    # Answer Keys
    path('answer-key/', include('apps.answer_keys.urls', namespace='answer_keys')),

    # Syllabus
    path('syllabus/', include('apps.syllabus.urls', namespace='syllabus')),

    # Blog
    path('blog/', include('apps.blog.urls', namespace='blog')),

    # User accounts
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),

    # Custom dashboard (will be built later)
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'
handler403 = 'apps.core.views.permission_denied'