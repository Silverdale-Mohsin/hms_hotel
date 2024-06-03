# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Reservation'
    _rec_name = 'reservation_ref'

    # HOTEL
    hotel = fields.Char(related='guest_id.hotel_id.name', string='Hotel', tracking=True)
    # GUEST
    guest_id = fields.Many2one('hotel.guest', string="Guest", tracking=True, required=True)
    gender = fields.Selection(related='guest_id.gender', tracking=True)
    guest_ref = fields.Char(string="Guest Ref.", help="Reference from guest records", tracking=True)
    guest_nationality = fields.Selection(related='guest_id.nationality', tracking=True)
    email = fields.Char(related='guest_id.email', tracking=True)
    phone_no = fields.Char(related='guest_id.phone_no', tracking=True)
    cnic_no = fields.Char(related='guest_id.cnic_no', tracking=True)
    passport_no = fields.Char(related='guest_id.passport_no', tracking=True)
    # ROOM
    room_id = fields.Many2one('hotel.room', string="Room", tracking=True)
    room_type = fields.Selection([('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')], string="Room Type", tracking=True)
    room_view_type = fields.Selection([('sea_view', 'Sea View'), ('city_view', 'City View'), ('garden_view', 'Garden View')], string="View Type", tracking=True)
    price_per_day = fields.Float(related='room_id.price_per_day', store=True, tracking=True)
    capacity = fields.Integer(related='room_id.capacity', tracking=True)
    # SERVICE
    service_ids = fields.Many2many('hotel.service', string="Services", tracking=True)
    service_total_price = fields.Float(string="Price (Services)", compute='_compute_totals', store=True, tracking=True)
    # SERVICE
    facility_ids = fields.Many2many('hotel.facility', string="Facilities", tracking=True)
    facility_total_price = fields.Float(string="Reservation Fee", compute='_compute_totals', store=True, tracking=True)
    # TAG
    tag_ids = fields.Many2many('hotel.tag', string="Tags", tracking=True)
    # PAYMENT
    receipt_number = fields.Char(string='Receipt Number', compute='_compute_receipt_number', tracking=True)
    # RESERVATION
    reservation_ref = fields.Char(string='Reference', default='New', tracking=True)
    reservation_date = fields.Date(string='Reservation Date', default=fields.Date.context_today, tracking=True)
    check_in_date = fields.Date(string='Check in Date', default=fields.Date.context_today, tracking=True)
    check_out_date = fields.Date(string='Check out Date', default=fields.Date.context_today, tracking=True)
    state = fields.Selection([('draft','Draft'),('pending','Pending'),('confirm','Confirmed'),('cancel','Cancelled'),('expire','Expired')], default="draft", string="Status", required=True, tracking=True)
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    duration = fields.Integer(string="Duration (Days)", compute='_compute_duration', tracking=True)
    special_requests = fields.Boolean(string="Special Requests", tracking=True)
    requests = fields.Text(string="Requests", tracking=True)
    currency_id = fields.Many2one('res.currency', related="guest_id.currency_id")
    price_subtotal = fields.Monetary(string="Price(Subtotal)", compute='_compute_totals', tracking=True)

    @api.model
    def create(self, vals):
        vals['reservation_ref'] = self.env['ir.sequence'].next_by_code('hotel.reservation')
        self._check_in_date_and_set_state(vals)
        res = super(HotelReservation, self).create(vals)
        self._handle_pending_state_create(res)
        return res

    def write(self, vals):
        for rec in self:
            self._handle_state_transition_and_room_change(rec, vals)
            self._check_in_date_and_set_state(vals)
            self._handle_state_cancel_or_expire(rec, vals)
        return super(HotelReservation, self).write(vals)

    def unlink(self):
        for rec in self:
            self._handle_pending_state_and_validate_deletable_state(rec)
            self._make_room_available_if_needed(rec)
        return super(HotelReservation, self).unlink()

    def _check_in_date_and_set_state(self, vals):
        if 'check_in_date' in vals:
            check_in_date = fields.Date.from_string(vals['check_in_date'])
            if check_in_date and check_in_date < fields.Date.today():
                vals['state'] = 'expire'
    def _handle_pending_state_create(self, reservation):
        if reservation.state == 'pending' and reservation.room_id:
            reservation.room_id.same_room_reserve += 1
            self._send_same_room_notification(reservation)
    def _handle_state_transition_and_room_change(self, reservation, vals):
        if 'state' in vals:
            if reservation.state == 'pending' and vals['state'] != 'pending' and reservation.room_id:
                reservation.room_id.same_room_reserve -= 1
            elif reservation.state != 'pending' and vals['state'] == 'pending' and reservation.room_id:
                reservation.room_id.same_room_reserve += 1
                self._send_same_room_notification(reservation)
            elif vals['state'] == 'confirm' and reservation.room_id:
                reservation.room_id.same_room_reserve = 0
        if 'room_id' in vals and vals['room_id'] != reservation.room_id.id and reservation.state == 'pending':
            if reservation.room_id:
                reservation.room_id.same_room_reserve -= 1
            new_room = self.env['hotel.room'].browse(vals['room_id'])
            new_room.same_room_reserve += 1
            self._send_same_room_notification(reservation, new_room)
    def _handle_state_cancel_or_expire(self, reservation, vals):
        if 'state' in vals and vals['state'] in ['cancel', 'expire']:
            if reservation.room_id:
                reservation.room_id.write({'is_available': True})
    def _handle_pending_state_and_validate_deletable_state(self, reservation):
        deletable_states = ['draft', 'expire']
        if reservation.state == 'pending' and reservation.room_id:
            reservation.room_id.same_room_reserve -= 1
        if reservation.state not in deletable_states:
            raise ValidationError(_("Can only delete Reservation in DRAFT or EXPIRE state"))
    def _make_room_available_if_needed(self, reservation):
        if reservation.room_id and not reservation.room_id.is_available:
            reservation.room_id.write({'is_available': True})

    @api.onchange('guest_id')
    def onchange_guest_id(self):
        self.guest_ref = self.guest_id.guest_ref

    def _compute_receipt_number(self):
        for reservation in self:
            payment = self.env['hotel.payment'].search([('reservation_id', '=', reservation.id)], limit=1)
            reservation.receipt_number = payment.receipt_number if payment else ''

    @api.depends('facility_ids', 'service_ids', 'price_per_day', 'duration')
    def _compute_totals(self):
        for record in self:
            record.facility_total_price = sum(facility.reservation_fee for facility in record.facility_ids)
            record.service_total_price = sum(service.cost for service in record.service_ids)
            record.price_subtotal = (record.price_per_day * record.duration) + record.service_total_price + record.facility_total_price

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 30)
            elif rec.state == 'pending':
                progress = random.randrange(30, 99)
            elif rec.state == 'confirm':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    @api.depends('check_in_date','check_out_date')
    def _compute_duration(self):
        for rec in self:
            if rec.check_out_date and rec.check_in_date:
                duration = (rec.check_out_date - rec.check_in_date).days
                rec.duration = duration
            else:
                rec.duration = 0

    def action_send_mail(self):
        template = self.env.ref('hms_hotel.reservation_mail_template')
        for rec in self:
            if rec.guest_id.email:
                template.send_mail(rec.id, force_send=True)

    def _send_same_room_notification(self, reservation, room=None):
        if room is None:
            room = reservation.room_id
        pending_reservations = self.search([('room_id', '=', room.id), ('state', '=', 'pending'), ('id', '!=', reservation.id)])
        template = self.env.ref('hms_hotel.reservation_same_room_mail_template')
        for res in pending_reservations:
            if res.guest_id.email:
                template.send_mail(res.id, force_send=True)

    def action_share_whatsapp(self):
        if not self.guest_id.phone_no:
            raise ValidationError(_("Missing Phone no. in Guest's Record"))
        message = 'Hi *%s*, your Reservation number is *%s*, Thank You' % (self.guest_id.name, self.reservation_ref)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.guest_id.phone_no, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            rec.room_id = False
            rec.room_type = False
            rec.room_view_type = False

    def action_pending(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'pending'