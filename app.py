import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apis import App
from routers import urls


app = App(urls=urls)