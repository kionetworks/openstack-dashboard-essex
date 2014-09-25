import os,sys

from django.core.wsgi import get_wsgi_application
path = '/usr/share/openstack-dasboard'
if path not in sys.path:
   sys.path.append(path)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openstack_dashboard.settings")
application = get_wsgi_application()

