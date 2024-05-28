# -*- coding: utf-8 -*-
import re
from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Guest'

    name = fields.Char(string="Name", tracking=True, required=True)
    guest_ref = fields.Char(string="Reference", default='New', tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')], string="Gender", tracking=True, required=True)
    email = fields.Char(string="Email", tracking=True, required=True)
    phone_no = fields.Char(string="Phone Number", tracking=True, required=True)
    emergency_contact_name = fields.Char(string="Name", tracking=True, required=True)
    emergency_contact_number = fields.Char(string="Phone Number", tracking=True, required=True)
    nationality = fields.Selection([('pakistan','Pakistan'),('other','Other')], string="Nationality", tracking=True, required=True)
    other_nationality = fields.Char(string="Other Nationality", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True, required=True)
    registration_date = fields.Date(string="Registration Date", tracking=True, default=fields.Date.context_today)
    age = fields.Integer(string="Age", compute='_compute_age', store=True, tracking=True)
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday', tracking=True)
    cnic_no = fields.Char(string="CNIC Number", tracking=True)
    passport_no = fields.Char(string="Passport Number", tracking=True)
    active = fields.Boolean(string="Active", default=True)
    image = fields.Image(string="Image", tracking=True)
    tag_ids = fields.Many2many('hotel.tag', string="Tags", tracking=True)
    marital_status = fields.Selection([('single','Single'),('married','Married')], string="Marital Status", tracking=True, required=True)
    reservation_ids = fields.One2many('hotel.reservation', 'guest_id', string="Reservations", tracking=True)
    card_ids = fields.One2many('hotel.guest.card', 'guest_id', string="Cards", tracking=True)
    reservation_count = fields.Integer(string="Reservation Count", compute='_compute_reservation_count', store=True, tracking=True)
    card_count = fields.Integer(string="Card Count", compute='_compute_card_count', store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")
    amount_total = fields.Monetary(string="Total", compute='_compute_amount_total', currency_field='currency_id', tracking=True)
    hotel_id = fields.Many2one('res.company', string='Hotel', required=True, tracking=True)

    @api.model
    def create(self, vals):
        vals['guest_ref'] = self.env['ir.sequence'].next_by_code('hotel.guest')
        self._validate_email(vals.get('email'))
        self._validate_phone_number(vals.get('phone_no'))
        self._validate_phone_number(vals.get('emergency_contact_number'))
        self._validate_identification(vals.get('cnic_no'), vals.get('passport_no'))
        return super(HotelGuest, self).create(vals)

    def write(self, vals):
        if 'email' in vals:
            self._validate_email(vals.get('email'))
        if 'phone_no' in vals:
            self._validate_phone_number(vals.get('phone_no'))
        if 'emergency_contact_number' in vals:
            self._validate_phone_number(vals.get('emergency_contact_number'))
        self._validate_identification(vals.get('cnic_no'), vals.get('passport_no'))
        return super(HotelGuest, self).write(vals)

    def _validate_email(self, email):
        email_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        if not email or not re.match(email_pattern, email):
            raise ValidationError(_("Entered email is not acceptable"))

    def _validate_phone_number(self, phone_number):
        phone_no_pattern = r"^(\+92|0|92)[0-9]{10}$"
        if not phone_number or not re.match(phone_no_pattern, phone_number):
            raise ValidationError(_("Entered phone number is not acceptable"))

    def _validate_identification(self, cnic_no, passport_no):
        cnic_pattern = r"^[0-9]{5}-[0-9]{7}-[0-9]$"
        passport_pattern = r"[A-Z]{2}[0-9]{7}"
        if cnic_no and cnic_no != 'False':
            if not re.match(cnic_pattern, cnic_no):
                raise ValidationError(_("Entered CNIC is not acceptable"))
        elif passport_no and passport_no != 'False':
            if not re.match(passport_pattern, passport_no):
                raise ValidationError(_("Entered passport number is not acceptable"))

    @api.onchange('nationality')
    def onchange_nationality(self):
        for rec in self:
            if rec.nationality == 'pakistan':
                rec.other_nationality = False
                rec.cnic_no = False
                rec.passport_no = False
            elif rec.nationality == 'other':
                rec.other_nationality = False
                rec.cnic_no = False
                rec.passport_no = False

    @api.depends('reservation_ids.price_subtotal', 'reservation_ids.state')
    def _compute_amount_total(self):
        for rec in self:
            pending_reservations = rec.reservation_ids.filtered(lambda r: r.state == 'pending')
            rec.amount_total = sum(line.price_subtotal for line in pending_reservations)

    @api.depends('reservation_ids')
    def _compute_reservation_count(self):
        reservation_read = self.env['hotel.reservation'].read_group(domain=[], fields=['guest_id'],groupby=['guest_id'])
        for rec in reservation_read:
            guest_id = rec.get('guest_id')[0]
            guest_rec = self.browse(guest_id)
            guest_rec.reservation_count = rec['guest_id_count']
            self -= guest_rec
        self.reservation_count = 0

    @api.depends('card_ids')
    def _compute_card_count(self):
        card_read = self.env['hotel.guest.card'].read_group(domain=[], fields=['guest_id'], groupby=['guest_id'])
        for rec in card_read:
            guest_id = rec.get('guest_id')[0]
            guest_rec = self.browse(guest_id)
            guest_rec.card_count = rec['guest_id_count']
            self -= guest_rec
        self.card_count = 0

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = datetime.today().date()
        for record in self:
            if record.date_of_birth:
                age = today.year - record.date_of_birth.year - (
                            (today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
                record.age = age
            else:
                record.age = 0

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('Not Acceptable!'))

    @api.ondelete(at_uninstall=False)
    def _check_reservations(self):
        for rec in self:
            if rec.reservation_ids:
                raise ValidationError(_("Caution! Cannot delete a Guest with Reservation"))

    def action_view_reservations(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reservations'),
            'res_model': 'hotel.reservation',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_guest_id': self.id},
            'domain': [('guest_id','=',self.id)],
        }

    def action_view_cards(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cards'),
            'res_model': 'hotel.guest.card',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_guest_id': self.id},
            'domain': [('guest_id','=',self.id)],
        }