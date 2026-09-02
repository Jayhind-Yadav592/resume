import os
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resumeforge.settings')

application = get_wsgi_application()

# Safe auto-migration execution on production startup
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    logging.getLogger(__name__).warning(f"Auto-migration notice: {e}")
