#!/bin/bash
# Run these commands on PythonAnywhere console

# Make sure we're in the project directory
cd ~/bnb_manager

# Install dependencies (if needed)
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# To create a superuser (uncomment and run if needed)
# python manage.py createsuperuser

# Reminder: After running these commands, go to the Web tab and reload the application 