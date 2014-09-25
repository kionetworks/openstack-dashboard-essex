from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from horizon import api
from keystoneclient.v2_0 import client as keystone_client

class UpdatePassword(forms.Form):
    '''
    Form to update user password
    '''

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'special'}),
        label=_("Old password")
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'special'}),
        label=_("New password")
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'special'}),
        label=_("Confirm new password")
    )

    def __init__(self, *args, **kwargs):
        '''
        Constructor to obtain the user from the request(sended in view)
        '''
        self.request = kwargs['request']
        kwargs.pop('request')
        self.user_id = self.request.user.id

        super(UpdatePassword, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        Check the old password and if new password confirmation is correct
        '''
        cleaned_data = super(UpdatePassword, self).clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        #user = api.keystone.user_get(self.request, self.user_id)
        try:
            keystone_user = keystone_client.Client(
                username=self.request.user.username,
                password=old_password,
                auth_url=settings.OPENSTACK_KEYSTONE_URL,
                tenant_id=self.request.session['tenant_id'],
            )
        except:
            self._errors["old_password"] = self.error_class([_('This is not your password, try again')])

        if new_password != confirm_new_password:
            self._errors["confirm_new_password"] = self.error_class([_('The passwords does not match.')])

        return cleaned_data
