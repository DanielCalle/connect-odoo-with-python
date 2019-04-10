# Imports
import xmlrpclib

# Connection
info = xmlrpclib.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = \
    info['host'], info['database'], info['user'], info['password']

# Calling methods
