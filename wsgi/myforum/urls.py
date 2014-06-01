from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = [

    url(r'^$', include('forum.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^user/', include('userprofile.urls', namespace='userprofile')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
