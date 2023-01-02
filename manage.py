#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
# Fetch the service account key JSON file contents
#cred = credentials.Certificate('secret.json')
# Initialize the app with a service account, granting admin privileges
#firebase_admin.initialize_app(cred, {
 #   'databaseURL': "https://community-bank-47a26-default-rtdb.europe-west1.firebasedatabase.app/"
#})

#ref = db.reference('/users')


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
