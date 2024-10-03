import os
import django
from Web.manage import main

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web.Web.settings')
django.setup()

main()
