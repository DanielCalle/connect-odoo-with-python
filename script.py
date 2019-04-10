#import xmlrpclib
import xmlrpc
import xmlrpc.client

def main():
    # Accedemos a Odoo
    uid = login()
    query(uid)

def login():
    # common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    res = common.version()
    print(res)
    uid = common.authenticate(db, username, password, {})
    print(uid)
    return uid

def query(uid):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    res = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True], ['customer', '=', True]]])
    print(res)
    a = models.execute_kw(db, uid, password, 'res.partner', 'read', [res], {'fields': ['name', 'country_id', 'comment']})
    print(a)

if __name__ == '__main__':
    # info = xmlrpclib.ServerProxy('https://demo.odoo.com/start').start()
    #info = xmlrpc.client.ServerProxy('https://localhost:8069/start').start()
    #url, db, username, password = \
    #    info['host'], info['database'], info['user'], info['password']

    url = 'http://localhost:8069'
    db = 'biopressman'
    username = 'zhong@ucm.es'
    password = "123456"

    main()

    print('Fin')
