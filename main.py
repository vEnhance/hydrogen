# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This file imports the WSGI-compatible object of your Django app,
# application from hserve/wsgi.py and renames it app so it is discoverable by
# App Engine without additional configuration.

from hserve.wsgi import application
app = application
