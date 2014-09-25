from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('openstack_dashboard.overrides.password.views',
    url(r'^$', 'index', name='index'),
    url(r'change$', 'index', name='change_password'),

)