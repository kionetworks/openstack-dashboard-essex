from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.settings import dashboard


class Password(horizon.Panel):
    name = _("Password")
    slug = 'password'

dashboard.Settings.register(Password)