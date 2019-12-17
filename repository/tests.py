from django.test import TestCase

# Create your tests here.

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoserver.settings")
    from django import setup
    setup()
    from repository import models
    print(dir(models))