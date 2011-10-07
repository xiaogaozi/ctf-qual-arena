import os
import sys
import site

ALLDIRS = ['/path/to/virtualenv/cqa/lib/python2.6/site-packages']

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = ['/path/to/cqa']
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'cqa.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
