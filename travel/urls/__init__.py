"""
Automatically discovers and imports each _urls.py
If app_name is defined, it includes the file using that as the namespace
If app_name is missing, it includes it as a plain set of URLs (as fallback)
"""

from django.urls import include, path
from importlib import import_module
import os

urlpatterns = []

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith('_urls.py') and filename != '__init__.py':
        module_name = f"{__package__}.{filename[:-3]}"
        module = import_module(module_name)

        # If the file is ajax_urls.py, namespace it properly
        if filename == 'ajax_urls.py':
            urlpatterns.append(path('ajax/', include((module.urlpatterns, 'travel_ajax'), namespace='travel_ajax')))
        else:
            urlpatterns.append(path('', include(module)))