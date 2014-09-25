# coding: utf-8
from django import forms
from django.core.mail import send_mail
import MySQLdb

from itertools import *
from django.template import loader
from utils import xor_crypt_string
from keystoneclient.v2_0 import client


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=(unicode("Email", 'utf-8')),
        widget=forms.TextInput(
            attrs={
                'class':'mws-login-password mws-textinput required',
                'placeholder': _(unicode("Email", 'utf-8')),
            }
        )
    )
    def clean(self):
        '''
        Check if the email exists
        '''
        cleaned_data = super(PasswordResetForm, self).clean()
        self.email = cleaned_data.get("email") 
        host = 'localhost'
        user = 'keystone'
        password = 'i36w59h3'
        database = 'keystone'
        conn = MySQLdb.Connection(db=database, host=host, user=user, passwd=password)
        mysql = conn.cursor()
        search = '"email": "%s"' % self.email
        sql = """SELECT id FROM user WHERE extra LIKE '%%""" + search + """%%'"""
        mysql.execute(sql)
        response = mysql.fetchall()
        if len(response) == 0:
            self._errors["email"] = self.error_class(['Imposible, No tienes una cuenta registrada'])
        else:
            self._id = response[0][0]
        return cleaned_data

    def save(self):
        subject = 'Recuperación de contraseña'
        key = 'g3w5i36'
        token = xor_crypt_string(self._id,key)
        context = {
            'token': token,
        }
        content = loader.render_to_string('content_email_template.html', context)
        from_email = 'soporte@kloudopen.com'
        send_mail(subject, content, from_email, [self.email])

class PasswordResetForm2(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(PasswordResetForm2, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label=(unicode("Password", 'utf-8')),
        widget=forms.PasswordInput(
            attrs={
                'class':'mws-login-password mws-textinput required',
                'placeholder': _(unicode("Password", 'utf-8')),
            }
        )
    )
    new_password2 = forms.CharField(
        label=(unicode("Password", 'utf-8')),
        widget=forms.PasswordInput(
            attrs={
                'class':'mws-login-password mws-textinput required',
                'placeholder': _(unicode("Confirm password", 'utf-8')),
            }
        )
    )

 
    def clean(self):
        cleaned_data = super(PasswordResetForm2, self).clean()

        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                self._errors["new_password2"] = self.error_class(['Imposible, las contraseñas no coinciden'])
        self.password = password1
        return cleaned_data

    def save(self):
        USER = 'admin'
        PASS = 'f346gqe0qww'
        TENANT_NAME = 'KioAdmin'
        KEYSTONE_URL = 'http://172.16.16.10:5000/v2.0'
        keystone = client.Client(username=USER,password=PASS,tenant_name=TENANT_NAME,auth_url=KEYSTONE_URL)
        keystone.authenticate()
        keystone.users.update_password(self.user_id, self.password)
