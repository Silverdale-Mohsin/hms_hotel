# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Booking'
    _rec_name = 'booking_ref'

    # GUEST
    guest_id = fields.Many2one('hotel.guest', string="Guest")
    guest_ref = fields.Char(string="Guest Ref.", help="Reference from guest records")
    guest_nationality = fields.Selection(related='guest_id.nationality')
    email = fields.Char(related='guest_id.email')
    phone_no = fields.Char(related='guest_id.phone_no')
    cnic_no = fields.Char(related='guest_id.cnic_no')
    passport_no = fields.Char(related='guest_id.passport_no')
    # FACILITY
    facility_id = fields.Many2one('hotel.facility', string="Facility")
    location = fields.Char(related='facility_id.location')
    available_hours = fields.Text(related='facility_id.available_hours')
    contact_person = fields.Many2one(related='facility_id.contact_person')
    contact_number = fields.Char(related='facility_id.contact_number')
    reservation_fee = fields.Float(related='facility_id.reservation_fee')
    # BOOKING
    booking_ref = fields.Char(string='Reference', default='New')
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time', default=fields.Datetime.now)
    state = fields.Selection([('pending','Pending'),('confirm','Confirmed'),('cancel','Cancelled')], default="pending", string="Status", required=True)
    total_cost = fields.Float(string='Cost')
    discount_amount = fields.Float(string='Discount')
    discount_reason = fields.Text(string='Reason')
    currency_id = fields.Many2one('res.currency', related="guest_id.currency_id")

    @api.model
    def create(self, vals):
        vals['booking_ref'] = self.env['ir.sequence'].next_by_code('hotel.booking')
        return super(HotelBooking, self).create(vals)

    def write(self, vals):
        return super(HotelBooking, self).write(vals)

    @api.onchange('guest_id')
    def onchange_guest_id(self):
        self.guest_ref = self.guest_id.guest_ref

    def action_share_whatsapp(self):
        if not self.guest_id.phone_no:
            raise ValidationError(_("Missing Phone no. in Guest's Record"))
        message = 'Hi *%s*, your Booking number is *%s*, Thank You' % (self.guest_id.name, self.booking_ref)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.guest_id.phone_no, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_confirm(self):
        for rec in self:
            if rec.state == 'pending':
                rec.state = 'confirm'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
        # action = self.env.ref('hms_hotel.action_hotel_cancel_reservation').read()[0]
        # return action