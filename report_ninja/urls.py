from django.conf.urls import patterns, include, url

# jpb, imported for report
from report import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'report_ninja.views.home', name='home'),
    # url(r'^report_ninja/', include('report_ninja.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # jpb, added for report app
    url(r'^$',views.index, name = 'index'),
    # jpb, example template for report
    url(r'^report/', views.report, name='report'),
    url(r'^client_report/get/(?P<client_id>\d+)/$','report.views.client_report'),
    # url(r'^client_crossshop/get/(?P<myid>\d+)/$','report.views.client_crossshop'),
    # jpb, below is for testing model inheritance
    url(r'^shops/get/(?P<myid>\d+)/$','report.views.shops'),
    
## jpb, these two views are working, don't remove.  They are used for creating the report.    
    url(r'^client_name/get/(?P<client_id>\d+)/$','report.views.client_name'),
    url(r'^client_sample/get/(?P<client_id>\d+)/$','report.views.client_sample'),

## jpb, these view generate various charts.  Don't remove them
   url(r'^client_crossshops/get/(?P<client_id>\d+)/$','report.views.client_crossshops'),

## jpb, this view generates the dmm charts for static use.  Don't remove it.   
   url(r'^client_dmm/get/(?P<client_id>\d+)/$','report.views.client_dmm'),
   
   ## jpb, this view generates the hitlist table for static use.  Don't remove it.   
   url(r'^client_hitlist/get/(?P<client_id>\d+)/$','report.views.client_hitlist'),

)
