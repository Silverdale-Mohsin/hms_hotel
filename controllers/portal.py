from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http, _
from odoo.tools import groupby as groupbyelement
from operator import itemgetter

class HotelGuestPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        rtn = super(HotelGuestPortal, self)._prepare_home_portal_values(counters)
        rtn['guest_count'] = request.env['hotel.guest'].search_count([])
        return rtn

    @http.route(['/my/guests', '/my/guests/page/<int:page>'], type='http', auth="user", website=True)
    def HotelGuestListView(self, page=1, sortby='id', search="", search_in="All", groupby="none", **kw):
        if not groupby:
            groupby = 'none'
        sorted_list = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': "Name", 'order': 'name'},
            'guest_ref': {'label': "Reference", 'order': 'guest_ref'}
        }
        search_list = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Name': {'label': "Name", 'input': 'Name', 'domain': [('name', 'ilike', search)]},
            'Reference': {'label': "Reference", 'input': 'Reference', 'domain': [('guest_ref', 'ilike', search)]}
        }
        groupby_list = {
            'none': {'input': 'none', 'label':_("None"), 'order': 1},
            'gender': {'input': 'gender', 'label':_("Gender"), 'order': 1},
            'marital_status': {'input': 'marital_status', 'label':_("Marital Status"), 'order': 1}
        }
        guest_group_by = groupby_list.get(groupby, {})
        default_order_by = sorted_list[sortby]['order']
        if groupby in ("gender", "marital_status"):
            guest_group_by = guest_group_by.get("input")
            default_order_by = guest_group_by+","+default_order_by
        else:
            guest_group_by = ''
        search_domain = search_list[search_in]['domain']
        guest_obj = request.env['hotel.guest']
        total_guest = guest_obj.search_count(search_domain)
        guest_url = '/my/guests'
        page_detail = pager(url=guest_url, total=total_guest, page=page, url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby}, step=10)
        guests = guest_obj.search(search_domain, limit=10, order=default_order_by, offset=page_detail['offset'])
        if guest_group_by:
            guests_group_list = [{guest_group_by: k, 'guests': guest_obj.concat(*g)} for k, g in groupbyelement(guests, itemgetter(guest_group_by))]
        else:
            guests_group_list = [{'guests': guests}]
        vals = {'group_guests': guests_group_list, 'page_name': 'guests_list_view', 'pager': page_detail, 'default_url': guest_url, 'groupby': groupby, 'searchbar_groupby': groupby_list, 'sortby': sortby, 'searchbar_sortings': sorted_list, 'search_in': search_in, 'searchbar_inputs': search_list, 'search': search}
        return request.render("hms_hotel.hotel_guests_list_view_portal", vals)

    @http.route(['/my/guest/<model("hotel.guest"):guest_id>'], type='http', auth="user", website=True)
    def HotelGuestFormView(self, guest_id, **kw):
        vals = {'guest': guest_id, 'page_name': 'guests_form_view'}
        guest_records = request.env['hotel.guest'].search([])
        guest_ids = guest_records.ids
        guest_index = guest_ids.index(guest_id.id)
        if guest_index != 0 and guest_ids[guest_index - 1]:
            vals['prev_record'] = '/my/guest/{}'.format(guest_ids[guest_index - 1])
        if guest_index < len(guest_ids) - 1 and guest_ids[guest_index + 1]:
            vals['next_record'] = '/my/guest/{}'.format(guest_ids[guest_index + 1])
        return request.render("hms_hotel.hotel_guests_form_view_portal", vals)

    @http.route(['/my/guest/print/<model("hotel.guest"):guest_id>'], type='http', auth="user", website=True)
    def HotelGuestReportPrint(self, guest_id, **kw):
        return self._show_report(model=guest_id, report_type='pdf', report_ref='hms_hotel.report_guest_detail', download=True)

class HotelReservationPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        rtn = super(HotelReservationPortal, self)._prepare_home_portal_values(counters)
        rtn['reservation_count'] = request.env['hotel.reservation'].search_count([])
        return rtn

    @http.route(['/my/reservations', '/my/reservations/page/<int:page>'], type='http', auth="user", website=True)
    def HotelReservationListView(self, page=1, sortby='id', search="", search_in="All", groupby="none", **kw):
        if not groupby:
            groupby = 'none'
        sorted_list = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'guest_id': {'label': "Guest Id", 'order': 'guest_id'},
            'reservation_ref': {'label': "Reference", 'order': 'reservation_ref'}
        }
        search_list = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Guest Id': {'label': "Guest Id", 'input': 'Guest Id', 'domain': [('guest_id', 'ilike', search)]},
            'Reference': {'label': "Reference", 'input': 'Reference', 'domain': [('reservation_ref', 'ilike', search)]}
        }
        groupby_list = {
            'none': {'input': 'none', 'label':_("None"), 'order': 1},
            'guest_id': {'input': 'guest_id', 'label':_("Guest Id"), 'order': 1},
            'state': {'input': 'state', 'label':_("State"), 'order': 1}
        }
        reservation_group_by = groupby_list.get(groupby, {})
        default_order_by = sorted_list[sortby]['order']
        if groupby in ("guest_id", "state"):
            reservation_group_by = reservation_group_by.get("input")
            default_order_by = reservation_group_by+","+default_order_by
        else:
            reservation_group_by = ''
        search_domain = search_list[search_in]['domain']
        reservation_obj = request.env['hotel.reservation']
        total_reservation = reservation_obj.search_count(search_domain)
        reservation_url = '/my/reservations'
        page_detail = pager(url=reservation_url, total=total_reservation, page=page, url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby}, step=10)
        reservations = reservation_obj.search(search_domain, limit=10, order=default_order_by, offset=page_detail['offset'])
        if reservation_group_by:
            reservations_group_list = [{reservation_group_by: k, 'reservations': reservation_obj.concat(*g)} for k, g in groupbyelement(reservations, itemgetter(reservation_group_by))]
        else:
            reservations_group_list = [{'reservations': reservations}]
        vals = {'group_reservations': reservations_group_list, 'page_name': 'reservations_list_view', 'pager': page_detail, 'default_url': reservation_url, 'groupby': groupby, 'searchbar_groupby': groupby_list, 'sortby': sortby, 'searchbar_sortings': sorted_list, 'search_in': search_in, 'searchbar_inputs': search_list, 'search': search}
        return request.render("hms_hotel.hotel_reservations_list_view_portal", vals)