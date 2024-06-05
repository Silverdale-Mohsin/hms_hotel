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
    print("Search Method")
    guests_search = models.execute_kw(db, uid, password, 'hotel.guest', 'search', [[]])
    print("Guests:", guests_search)
    # guests_search = models.execute_kw(db, uid, password, 'hotel.guest', 'search', [[['gender', '=', 'male']]])
    # print("Male Guests:", guests_search)
    # guests_search = models.execute_kw(db, uid, password, 'hotel.guest', 'search', [[['gender', '=', 'female']]])
    # print("Female Guests:", guests_search)

    # Search-Count Method
    print("Search-Count Method")
    guests_search_count = models.execute_kw(db, uid, password, 'hotel.guest', 'search_count', [[]])
    print("Guests:", guests_search_count)
    # guests_search_count = models.execute_kw(db, uid, password, 'hotel.guest', 'search_count', [[['gender', '=', 'male']]])
    # print("Male Guests:", guests_search_count)
    # guests_search_count = models.execute_kw(db, uid, password, 'hotel.guest', 'search_count', [[['gender', '=', 'female']]])
    # print("Female Guests:", guests_search_count)

    # Read Method
    print("Read Method")
    guests_record = models.execute_kw(db, uid, password, 'hotel.guest', 'read', [guests_search], {'fields': ['name', 'guest_ref', 'gender']})
    print("Guests:", guests_record)

    # Search-Read Method
    print("Search-Read Method")
    guests_search_read = models.execute_kw(db, uid, password, 'hotel.guest', 'search_read', [[]], {'fields': ['id', 'name', 'guest_ref']})
    print("Guests:", guests_search_read)

    # Create Method
    print("Create Method")
    # vals = {
    #     "hotel_id": 3,
    #     "name": "External APIs",
    #     "gender": "female",
    #     "marital_status": "single",
    #     "email": "externalapi@gmail.com",
    #     "phone_no": "03001234567",
    #     "date_of_birth": "2000-10-25",
    #     "nationality": "pakistan",
    #     "cnic_no": "38401-1234567-8",
    #     "emergency_contact_name": "RestApi",
    #     "emergency_contact_number": "03339874563"
    # }
    # created_id = models.execute_kw(db, uid, password, 'hotel.guest', 'create', [vals])
    # print("Created Record", created_id)

    # Write/Update Method
    print("Write/Update Method")
    id = models.execute_kw(db, uid, password, 'hotel.guest', 'search', [[['name', '=', "External API"]]])
    models.execute_kw(db, uid, password, 'hotel.guest', 'write', [id, {'name': "API Updated"}])
    # models.execute_kw(db, uid, password, 'hotel.guest', 'write', [[46], {'mobile': "03001122333"}])

    # Unlink/Delete Method
    print("Unlink/Delete Method")
    # models.execute_kw(db, uid, password, 'hotel.guest', 'unlink', [[11]])
else:
    print("Authentication Failed!")