# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response

def error_response(code, message):
    # This function returns a dictionary formatted as an error response with the provided status code and message.
    return {
        "success": False,
        "status": code,
        "error": message
    }
def format_query(query):
    # This function takes a query dictionary and converts it into a list format suitable for Odoo domain filters.
    req_result = []
    for key, value in query.items():
        req_result.extend([key, '=', value])
    return req_result

class Restapi(http.Controller):
    @http.route('/restapi', auth='public')
    def index(self, **kw):
        return "Server up and running"

    @http.route('/restapi/auth', auth='none', methods=['POST'], csrf=False, type='json')
    def authenticate_user(self, **post_data):
        try:
            if 'db' not in post_data and 'username' not in post_data and 'password' not in post_data:
                return error_response(400, "Missing input check again")
            authenticate = request.session.authenticate(post_data['db'], post_data['username'], post_data['password'])
            if not authenticate:
                return error_response(400, "Invalid credentials cannot authenticate")
            session_info = request.env['ir.http'].session_info()
            return Response(json.dumps(session_info), status=200, content_type='application/json')
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")

    @http.route('/restapi/get-all', auth='user', methods=['GET'])
    def get_all(self, **kw):
        try:
            data = request.env['hotel.guest'].search_read([])
            if not data:
                return error_response(400, "No data found")
            response_data = {
                'success': True,
                'message': 'All guests retrieved',
                'data': data
            }
            return Response(json.dumps(response_data, default=str), status=200, content_type='application/json')
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")

    @http.route('/restapi/get-data/<int:id>', auth='user', methods=['GET'])
    def get_data(self, id, **params):
        try:
            if not id:
                return error_response(400, "No query params found")
            formatted_params = format_query(params)
            data_found = request.env['hotel.guest'].browse(id).read()
            if not data_found:
                return error_response(400, "Data not found with requested params")
            response_data = {
                'status': 'Success',
                'message': 'Data found',
                'data': data_found
            }
            return Response(json.dumps(response_data, default=str), status=200, content_type='application/json')
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")

    @http.route('/restapi/create', auth='user', csrf=False, methods=['POST'], type='json')
    def create(self, **post_data):
        try:
            if 'name' not in post_data:
                return error_response(400, "No name found in request")
            created_data = request.env['hotel.guest'].create(post_data)
            return json.dumps({"message": "User created", "status": 201, "success": "True", "data": created_data}, default=str)
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")

    @http.route('/restapi/update/<int:id>', auth='user', csrf=False, methods=['PUT'], type='json')
    def update_record(self, id, **params):
        try:
            if not id:
                return error_response(400, "No id in query path")
            update_rec = request.env['hotel.guest'].browse(id).write(params)
            print(update_rec, "rec")
            if not update_rec:
                return error_response(400, "Id not exists")
            return Response(json.dumps({"success": True, "message": "successfully updated"}, default=str), status=200, content_type='application/json')
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")

    @http.route('/restapi/delete/<int:id>', auth='user', csrf=False, methods=['DELETE'])
    def delete_record(self, id, **params):
        try:
            if not id:
                return error_response(400, "No id in query path")
            delete_rec = request.env['hotel.guest'].browse(id)
            if not delete_rec:
                return error_response(400, "Id not exists")
            delete_rec.unlink()
            return Response(json.dumps({"success": True, "message": "successfully deleted"}, default=str), status=200, content_type='application/json')
        except Exception as e:
            return error_response(500, f"Server error: {str(e)}")
