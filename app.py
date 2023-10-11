import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apis import App
from routers import urls
from wsgi.auth.jwt import JwtAuthentication

app = App(urls=urls)

app.config['DEFAULT_AUTHENTICATION_CLASSE'] = JwtAuthentication