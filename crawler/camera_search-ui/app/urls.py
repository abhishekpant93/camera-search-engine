from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
	url(r'^search/$', views.search, name='search'),
	url(r'^search_results/$', views.search_results, name='search_results'),
	# url(r'^summary/$', views.summary, name='summary'),
	# url(r'^summary_api/$', views.summary_api, name='summary_api'),
	# url(r'^api_result/$', views.api_result, name='api_result') 
)