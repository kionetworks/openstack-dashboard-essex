from django import shortcuts
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from horizon import api

from forms import UpdatePassword

def index(request):
    form = UpdatePassword(request=request)
    if request.method == 'POST':
        form = UpdatePassword(request=request, data=request.POST)
        if form.is_valid():
            if api.keystone_can_edit_user():
                api.user_update_password(
                    request,
                    request.user.id,
                    form.cleaned_data['new_password'],
                    admin=True
                )
                request.user_logout()
                return shortcuts.redirect('/auth/login')
    return shortcuts.render(request, 'password/settings.html', {
        'form': form,
    })
