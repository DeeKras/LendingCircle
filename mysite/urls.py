from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lendborrow.views.index', name='index'),
    url(r'^register/$', 'lendborrow.views.register', name='register'),
    url(r'^login/$', 'lendborrow.views.user_login', name='login'),
    url(r'^borrow/$', 'lendborrow.views.borrow', name='borrow_transactions'),
    url(r'^borrow/edit', 'lendborrow.views.borrow_edit', name='borrow_transactions'),
    url(r'^returned/','lendborrow.views.returned', name='returned'),
    url(r'^reports/', 'lendborrow.views.display_reports', name='reports'),
    url(r'^selected/', 'lendborrow.views.record_selected', name='record_selected'),
)
