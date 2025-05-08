# PythonAnywhere local settings for bnb_manager
DEBUG = False

# Replace 'yourusername' with your actual PythonAnywhere username
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/yourusername/bnb_manager/db.sqlite3',
    }
}

# Static files configuration
STATIC_ROOT = '/home/yourusername/bnb_manager/static'
STATIC_URL = '/static/'

# Media files configuration (if needed)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/bnb_manager/media'

# Set a proper time zone if needed
TIME_ZONE = 'UTC'

# For production, use a proper secret key
# SECRET_KEY = 'your-secure-key-here' 