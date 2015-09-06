from django.conf.urls import patterns, include, url
from django.contrib import admin
from muraki import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'segregation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.index, name="index"),
    
    url(r'^muraki_graph/$', views.muraki_graph, name="muraki_graph"),
    
    url(r'^muraki/$', views.index, name="muraki_graph"),
    
    url(r'^in_concentration_graph/$', views.in_concentration_graph, name="in_concentration_graph"),
    
    url(r'^in_energies_graph/$', views.in_energies_graph, name="in_energies_graph"),
    
    url(r'^strained_well/$', views.strained_well, name="strained_well"),
)
