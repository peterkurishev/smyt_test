from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smyt_test.settings')

from dj_static import Cling

application = Cling(get_wsgi_application())