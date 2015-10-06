from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
#from CongressScore.forms import NonEmptySearchForm
#from haystack.forms import ModelSearchForm
#from haystack.query import SearchQuerySet
#from haystack.views import SearchView, search_view_factory
from CongressScore import views

#import xadmin
#xadmin.autodiscover()
#from xadmin.plugins import xversion
#xversion.register_models()

from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SpaceScore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^CongressScore/', include('CongressScore.urls')),
    url(r'^$', views.HomeView, name='home'),
    url(r'^methodology.html', views.HomeView, name='home'),
	(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^search/', 
    #SearchView(template='search/search.html',searchqueryset=sqs,form_class=NonEmptySearchForm), name='haystack_search')
)
urlpatterns += patterns('', ('', include('django_evercookie.urls')),)