#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AOEP.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# In Django shell (python manage.py shell)
from django.contrib.auth.models import User
from Core.models import UserProfile

# Create profiles for users who don't have one
for user in User.objects.all():
    if not hasattr(user, 'userprofile'):
        # Create with default 0% progress or set a specific value
        UserProfile.objects.create(user=user, ebook_completion_percentage=0)