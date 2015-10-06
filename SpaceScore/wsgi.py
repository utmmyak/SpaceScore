#import sys, logging
#logging.basicConfig(stream = sys.stderr)

import sys
sys.path.insert(0, "/opt/apps/SpaceScore-env/site/")
sys.path.insert(0, "/opt/apps/SpaceScore-env/lib/python2.7/")

SITE_DIR = '/opt/apps/SpaceScore-env/site/'
import site
site.addsitedir(SITE_DIR) 

import os
import sys
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'SpaceScore.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
