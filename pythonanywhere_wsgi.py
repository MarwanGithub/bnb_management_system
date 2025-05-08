# PythonAnywhere WSGI configuration file
# Copy the contents of this file to the WSGI file on PythonAnywhere
# Replace 'yourusername' with your actual PythonAnywhere username

import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/bnb_manager'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable to tell Django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'bnb_manager.settings'

# Set up Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 