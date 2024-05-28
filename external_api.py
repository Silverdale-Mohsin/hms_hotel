import xmlrpc.client

url = 'http://localhost:8069'
db = 'Odoo16'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
if uid:
    print("Authentication Success!")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Search Method
    # partners_search = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
    # print("Partners Search:", partners_search)
    # partners_search = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
    # print("Partners Search:", partners_search)
    # partners_search = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]], {'offset': 10, 'limit': 5})
    # print("Partners Search:", partners_search)

    # Search-Count Method
    # partners_search_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[]])
    # print("Partners Search Count:", partners_search_count)
    # partners_search_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
    # print("Partners Search Count:", partners_search_count)

    # Read Method
    # partners_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners_search], {'fields': ['name', 'country_id', 'comment']})
    # print("Partner Read Record:", partners_rec)

    # Search-Read Method
    # partners_search_read = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['id', 'name']})
    # print("Partner Search-Read Record:", partners_search_read)

    # vals = {
    #     'name': "Odoo Mates External APIs",
    #     'email': "odoomates@hotmail.com"
    # }
    # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
    # print("Created Record", created_id)

    # Write/Update Method
    # id = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'odoomates@hotmail.com']]])
    # models.execute_kw(db, uid, password, 'res.partner', 'write', [id, {'mobile': "03211231230"}])
    # models.execute_kw(db, uid, password, 'res.partner', 'write', [[46], {'mobile': "03001122333"}])

    # Unlink/Delete Method
    # models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[47]])
else:
    print("Authentication Failed!")