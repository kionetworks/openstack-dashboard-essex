# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
URL patterns for the OpenStack Dashboard.
"""

from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import horizon

from views import forgot_password_reset
from openstack_dashboard.overrides.password import urls as password_urls

urlpatterns = patterns('',
    url(r'^$', 'openstack_dashboard.views.splash', name='splash'),
    url(r'^forgot-password/?$', 'openstack_dashboard.views.forgot_password', name='forgot_password'),
    url(r'^forgot-password-sent/?$', 'openstack_dashboard.views.forgot_password_sent', name='forgot_password_sent'),
    url(r'^forgot-password-reset/(?P<token>.*)/?$', forgot_password_reset, name='forgot_password_reset'),
    url(r'^forgot-password-reset-complete/?$', 'forgot_password_reset_complete', name='forgot_password_reset_complete'),
    url(r'^qunit/$',
        'openstack_dashboard.views.qunit_tests',
        name='qunit_tests'),
    url(r'', include(horizon.urls)),
    url(r'settings/password/', include(password_urls))
)

# Development static app and project media serving using the staticfiles app.
urlpatterns += staticfiles_urlpatterns()

# Convenience function for serving user-uploaded media during
# development. Only active if DEBUG==True and the URL prefix is a local
# path. Production media should NOT be served by Django.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Javascript Translations
js_info_dict = {
    'packages': ('openstack_dashboard',),
}

urlpatterns += patterns('',
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)

