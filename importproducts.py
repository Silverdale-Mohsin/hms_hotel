import xmlrpc.client
import csv

server = "http://localhost:8069"
database = "odoo15"
user = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % server)
# common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
# In systems like Odoo, this endpoint might be used to authenticate users, start and close sessions, or retrieve metadata about the available models.
print (common.version())

uid =common.authenticate(database,user,password,{})
print(uid)

# OdooApi = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')
OdooApi = xmlrpc.client.ServerProxy('%s//xmlrpc/2/object' % server)
# For instance, you might use this endpoint to interact with specific records like creating a new customer, updating a product, or deleting an invoice.

product_count = OdooApi.execute_kw(database,uid,password,'vetapps.animal','search_count',[[]])
print(f"Product Count : {product_count}")

species_count = OdooApi.execute_kw(database,uid,password,'vetapps.species','search_count',[[]])
print(f"Species Count : {species_count}")

species = OdooApi.execute_kw(database,uid,password,'vetapps.animal','search',[[['species_id', '=', 'Cat']]])
print(f"Species : {species}")

species_detail = OdooApi.execute_kw(database,uid,password,'vetapps.animal','read',[species])
print(f"Cats : {species_detail}")

species_name = OdooApi.execute_kw(database,uid,password,'vetapps.animal','read',[species],{'fields':["name"]})
print(f"Cats : {species_name}")

Filename = "importdata.csv"
reader = csv.reader(open(Filename,'r'))
# species_id_filter = OdooApi.execute_kw(database, uid, password, 'vetapps.species', 'search', [[['name', '=', 'Dog']]])
# breed_id_filter = OdooApi.execute_kw(database, uid, password, 'vetapps.breed', 'search', [[['name', '=', 'Husky']]])
# # print(species_id_filter)
# # print(breed_id_filter)
#
# for row in reader:
#     name = row[0]
#     # breed = row[1]
#     animal_ids = OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'search',[[['name', '=', name]]])
#     # filter = [[('name','=',name)]]
#     # species_id_data = OdooApi.execute_kw(database, uid, password, 'vetapps.species', 'search', filter)
#     if animal_ids:
#         record = {'name': name, 'breed_id':breed_id_filter[0], 'species_id': species_id_filter[0]}
#         OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'write', [animal_ids ,record])
#         # species_data = OdooApi.execute_kw(database, uid, password, 'vetapps.species', 'create', record)
#         # print(f"Record Inserted: {name}")
#         print("Updated")
#     else:
#         OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'create', [{'name': name, 'breed_id': breed_id_filter[0], 'species_id': species_id_filter[0]}])
#         # print("Already Entered")
#         print("Created")
# Assuming OdooApi.execute_kw(database, uid, password, 'vetapps.breed', 'search', [[['name', '=', 'Husky']]]) returns breed IDs

# Define breed_ids outside the loop
breed_ids = {}
for row in reader:
    animal_names = row[0].split(',')  # Split the string into a list of animal names
    breed_names = row[1].split(',')  # Split the string into a list of breed names
    print("Animal Names:", animal_names)
    print("Breed Names:", breed_names)
    for breed_name in breed_names:
        breed_id_filter = OdooApi.execute_kw(database, uid, password, 'vetapps.breed', 'search',[[['name', '=', breed_name]]])
        if breed_id_filter:
            breed_ids[breed_name] = breed_id_filter[0]
    species_id_filter = OdooApi.execute_kw(database, uid, password, 'vetapps.species', 'search',[[['name', '=', 'Bird']]])

    for name, breed_name in zip(animal_names, breed_names):
        if breed_name in breed_ids:
            breed_id = breed_ids[breed_name]
            animal_ids = OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'search',[[['name', '=', name]]])
            if animal_ids:
                record = {'name': name, 'breed_id': breed_id, 'species_id': species_id_filter[0]}
                OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'write', [animal_ids, record])
                print("Updated")
            else:
                OdooApi.execute_kw(database, uid, password, 'vetapps.animal', 'create',[{'name': name, 'breed_id': breed_id, 'species_id': species_id_filter[0]}])
                print("Created")
        else:
            print(f"Breed '{breed_name}' not found in the system.")

