import os
import django
from pylint import lint

# Set the DJANGO_SETTINGS_MODULE environment
# variable to your Django settings module
os.environ.setdefault
("DJANGO_SETTINGS_MODULE",
 "django_share_the_plate.settings"
 )
django.setup()

# Run Pylint with your custom .pylintrc and the Django app name
lint.Run(["--rcfile=.pylintrc", "share_the_plate"])
