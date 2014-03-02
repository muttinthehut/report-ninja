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
    
    # jpb, added for report app home page - don't remove
    url(r'^$',views.index, name = 'index'),


    
## jpb, these two views are working, don't remove.  They are used for creating the report.    
    url(r'^client_name/get/(?P<client_id>\d+)/$','report.views.client_name'),
    url(r'^client_sample/get/(?P<client_id>\d+)/$','report.views.client_sample'),


## jpb, this view gnerate the cross shop chart for static use. Don't remove it.

    url(r'^client_crossshops/get/(?P<client_id>\d+)/$','report.views.client_crossshops'),

## jpb, this view generates the dmm charts for static use.  Don't remove it.   
   url(r'^client_dmm/get/(?P<client_id>\d+)/$','report.views.client_dmm'),
   
   ## jpb, this view generates the hitlist table for static use.  Don't remove it.   
   url(r'^client_hitlist/get/(?P<client_id>\d+)/$','report.views.client_hitlist'),
   
## jpb, these URLs are for the user portal login and logout
    # url(r'^login/$','django.contrib.auth.views.login'),
    # url(r'^logout/$','report.views.logout_page'),
    # url(r'^portal/','report.views.portal_page'),
    # url(r'^auth_password_reset/$','django.contrib.auth.views.password_change'),
    # url(r'^password_changed/$','django.contrib.auth.views.password_change_done'),
    # jpb, 2/24 register page working 
    url(r'^register/$','report.views.register',name='register'), 
    # jpb, 2/24 added for login
    url(r'^login/$','report.views.user_login',name='login'),
    # jpb, 2/24 added for logout
    url(r'^logout/$','report.views.user_logout',name='logout'), 
    

## jpb, this URL is for user dashboard
    url(r'^dashboard/$','report.views.dashboard',name='dashboard'),

## jpb, these are for sending email reports
    url(r'^sendmktrpt/(?P<client_id>\d+)/$','report.views.sendmktrpt',name='sendmktrpt'),

## NOT USED BELOW
       # jpb, example template for report.  Old and can be removed.
        url(r'^report/', views.report, name='report'),

    # sample only, not used 
    url(r'^client_report/get/(?P<client_id>\d+)/$','report.views.client_report'),



)
