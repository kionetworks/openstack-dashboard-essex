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
Views for home page.
"""
from django import shortcuts
from django.views.decorators import vary

import horizon
from horizon.views import auth as auth_views
from forgot_password_forms import PasswordResetForm, PasswordResetForm2
from utils import xor_decrypt_string
from django.http import Http404
import MySQLdb


def qunit_tests(request):
    return shortcuts.render(request, "qunit.html")


def user_home(user):
    if user.admin:
        return horizon.get_dashboard('syspanel').get_absolute_url()
    return horizon.get_dashboard('nova').get_absolute_url()


@vary.vary_on_cookie
def splash(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(user_home(request.user))
    form, handled = auth_views.Login.maybe_handle(request)
    if handled:
        return handled
    request.session.clear()
    return shortcuts.render(request, 'splash.html', {'form': form})

def forgot_password(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return shortcuts.render(request, 'forgot_password_email_sent.html', {})
    return shortcuts.render(request, 'forgot_password.html', {'form': form})

def forgot_password_sent(request):
    return shorcuts.render(request, 'forgot_password_sent.html', {})

def forgot_password_reset(request, token):
    key = 'g3w5i36'
    _id = xor_decrypt_string(token, key)
    host = 'localhost'
    user = 'keystone'
    password = 'i36w59h3'
    database = 'keystone'
    conn = MySQLdb.Connection(db=database, host=host, user=user, passwd=password)
    mysql = conn.cursor()
    sql = "SELECT id FROM user WHERE id='%s'" % _id
    mysql.execute(sql)
    response = mysql.fetchall()
    if len(response) == 0:
        raise Http404
    form = PasswordResetForm2()
    if request.method == 'POST':
        form = PasswordResetForm2(request.POST, user_id=_id)
        if form.is_valid():
            form.save()
            return shortcuts.render(request, 'forgot_password_reset_done.html', {})
    return shortcuts.render(request, 'forgot_password_reset.html', {'form': form, 'token': token})

