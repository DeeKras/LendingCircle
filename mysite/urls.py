from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lendborrow.views.index', name='index'),
    url(r'^register/$', 'lendborrow.views.register', name='register'),
    # url(r'^new/user/$', 'lendborrow.views.CreateUserView.as_view()', name='user-new',),
    # url(r'^edit/user/(?P<pk>\d+)/$', 'lendborrow.views.UpdateUserView.as_view()', name='user-edit',),
    url(r'^login/$', 'lendborrow.views.user_login', name='login'),
    url(r'^borrow/', 'lendborrow.views.borrow', name='new_borrow'),
)
