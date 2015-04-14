from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'camera_search.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('app.urls', namespace='app')),
    url(r'^admin/', include(admin.site.urls)),
)
