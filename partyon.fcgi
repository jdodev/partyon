#!/home1/jdoavil1/python/bin/python
import sys, os

sys.path.insert(0, "/home1/jdovil1/python")
sys.path.insert(13, "/home1/jdoavil1/public_html/sitios/partyon")

os.environ['DJANGO_SETTINGS_MODULE'] = 'partyon.settings'
os.environ['PYTHON_EGG_CACHE'] = 'tmp/trac-eggs'
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
