# import xmlrpclib
import xmlrpc
import xmlrpc.client


def login():
    # common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    res = common.version()
    print(res)
    uid = common.authenticate(db, username, password, {})
    print("uid:", uid)
    return uid

def calling_methods(uid, models):
    return models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception' : False})

def list_records(uid, models):
    return models.execute_kw(db, uid, password, 'res.partner', 'search',
                      [[
                        ['is_company', '=', True],
                        ['customer', '=', True]
                      ]])

def pagination(uid, models):
    return models.execute_kw(db, uid, password, 'res.partner',
                             'search',
                             [[
                               ['is_company', '=', True],
                               ['customer', '=', True]
                             ]],
                             {'offset': 10, 'limit': 5})

def count_records(uid, models):
    return models.execute_kw(db, uid, password,
                             'res.partner', 'search_count',
                             [[
                               ['is_company', '=', True],
                               ['customer', '=', True]
                             ]])

def read_records(uid, models):
    ids = models.execute_kw(db, uid, password,
                            'res.partner', 'search',
                            [[
                                ['is_company', '=', True],
                                ['customer', '=', True]
                            ]],
                            {'limit': 1})
    [record] = models.execute_kw(db, uid, password,
                                 'res.partner', 'read', [ids])
    # count the number of fields fetched by default
    len(record)
    return models.execute_kw(db, uid, password,
                             'res.partner', 'read', [ids],
                             {'fields': ['name', 'country_id', 'comment']})

def listing_records_fields(uid, models):
    return models.execute_kw(db, uid, password, 'res.partner',
                             'fields_get', [],
                             {'attributes': ['string', 'help', 'type']})

def search_and_read(uid, models):
    return models.execute_kw(db, uid, password,
                             'res.partner', 'search_read',
                             [[
                                ['is_company', '=', True],
                                ['customer', '=', True]
                             ]],
                             {
                                'fields': ['name', 'country_id', 'comment'],
                                'limit': 5
                                })

def create_records(uid, models):
    id = models.execute_kw(db, uid, password,
                           'res.partner', 'create',
                           [{'name': "New Partner"}])
    return id

def update_records(uid, models, id):
    models.execute_kw(db, uid, password, 'res.partner',
                      'write',
                      [
                        [id],
                        {'name': "Newer partner"}
                      ])
    return models.execute_kw(db, uid, password,
                             'res.partner', 'name_get', [[id]])

def delete_records(uid, models, id):
    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
    # check if the deleted record is still in the database
    return models.execute_kw(db, uid, password,
                             'res.partner', 'search', [[['id', '=', id]]])

def inspection_and_introspection(uid, models):
  if (False) :
    models.execute_kw(db, uid, password, 'ir.model', 'create', [{
        'name': "Custom Model",
        'model': "x_custom_model",
        'state': 'manual',
    }])
  return models.execute_kw(db, uid, password, 'x_custom_model', 'fields_get', [], {'attributes': ['string', 'help', 'type']})

def workflow_manipulations(uid, models):
    client = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                               [[('customer', '=', True)]],
                               {
                                'limit': 1,
                                'fields': [ 'property_account_receivable',
                                            'property_payment_term',
                                            'property_account_position']
                                })[0]
    invoice_id = models.execute_kw(db, uid, password,
                                   'account.invoice',
                                   'create',
                                   [{
                                        'partner_id': client['id'],
                                        'account_id': client['property_account_receivable'][0],
                                        'invoice_line': [(0, False, {'name': "AAA"})]
                                    }])

    return models.exec_workflow(db, uid, password, 'account.invoice',
                                'invoice_open', invoice_id)

def report_printing(uid, models):
    invoice_ids = models.execute_kw(db, uid, password, 'account.invoice',
                                    'search',
                                    [[
                                        ('type', '=', 'out_invoice'),
                                        ('state', '=', 'open')]
                                    ])
    report = xmlrpc.ServerProxy('{}/xmlrpc/2/report'.format(url))
    result = report.render_report(db, uid, password, 'account.report_invoice',
                                  invoice_ids)
    return result['result'].decode('base64')

def main():
    # Accedemos a Odoo
    print("login")
    uid = login()
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    print("calling_methods")
    print(calling_methods(uid, models))

    print("list_records")
    print(list_records(uid, models))

    print("pagination")
    print(pagination(uid, models))

    print("count_records")
    print(count_records(uid, models))

    print("read_records")
    print(read_records(uid, models))

    print("listing_records_fields")
    print(listing_records_fields(uid, models))

    print("search_and_read")
    print(search_and_read(uid, models))

    print("create_records")
    id = create_records(uid, models)
    print(id)

    print("update_records")
    print(update_records(uid, models, id))

    print("delete_records")
    print(delete_records(uid, models, id))

    print("inspection_and_introspection")
    print(inspection_and_introspection(uid, models))



if __name__ == '__main__':
    # info = xmlrpclib.ServerProxy('https://demo.odoo.com/start').start()
    # info = xmlrpc.client.ServerProxy('https://localhost:8069/start').start()
    # url, db, username, password = \
    #    info['host'], info['database'], info['user'], info['password']

    url = 'http://localhost:8069'
    db = 'biopressman'
    username = 'zhong@ucm.es'
    password = "123456"

    main()

    print('End')
