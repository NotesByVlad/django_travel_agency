from django.urls import include, path
from importlib import import_module
import os

urlpatterns = []

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith('_urls.py') and filename != '__init__.py':
        module_name = f"{__package__}.{filename[:-3]}"  # remove '.py'
        module = import_module(module_name)
        urlpatterns.append(path('', include(module)))