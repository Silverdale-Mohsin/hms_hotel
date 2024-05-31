# -*- coding: utf-8 -*-
import re
from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Hotel(models.Model):
    _inherit = 'res.company'

    is_hotel = fields.Boolean(string="is_Hotel", default=True, tracking=True)
    bank_account_ids = fields.One2many('hotel.bank.account', 'hotel_id', string='Bank Accounts')
    bank_account_count = fields.Integer(string="Bank Account Count", compute='_compute_bank_account_count', store=True)
    employee_ids = fields.One2many('res.users', 'hotel_id', string='Employees')
    employee_count = fields.Integer(string="Employee Count", compute='_compute_employee_count', store=True)
    room_ids = fields.One2many('hotel.room', 'hotel_id', string='Rooms')
    room_count = fields.Integer(string="Room Count", compute='_compute_room_count', store=True)
    payment_ids = fields.One2many('hotel.payment', 'hotel_id', string='Payments')
    payment_count = fields.Integer(string="Payment Count", compute='_compute_payment_count', store=True)
    guest_ids = fields.One2many('hotel.guest', 'hotel_id', string='Guests')
    guest_count = fields.Integer(string="Guest Count", compute='_compute_guest_count', store=True)

    @api.model
    def create(self, vals):
        vals['guest_ref'] = self.env['ir.sequence'].next_by_code('hotel.guest')
        self._validate_email(vals.get('email'))
        self._validate_phone_number(vals.get('phone'))
        return super(Hotel, self).create(vals)

    def write(self, vals):
        if 'email' in vals:
            self._validate_email(vals.get('email'))
        if 'phone' in vals:
            self._validate_phone_number(vals.get('phone'))
        return super(Hotel, self).write(vals)

    def _validate_email(self, email):
        email_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        if not email or not re.match(email_pattern, email):
            raise ValidationError(_("Entered email is not acceptable"))

    def _validate_phone_number(self, phone_number):
        phone_no_pattern = r"^(\+92|0|92)[0-9]{10}$"
        if not phone_number or not re.match(phone_no_pattern, phone_number):
            raise ValidationError(_("Entered phone number is not acceptable"))

    @api.depends('bank_account_ids')
    def _compute_bank_account_count(self):
        for record in self:
            record.bank_account_count = self.env['hotel.bank.account'].search_count([('hotel_id', '=', record.id)])
    def action_view_bank_account(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Accounts'),
            'res_model': 'hotel.bank.account',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_hotel_id': self.id},
            'domain': [('hotel_id','=',self.id)],
        }

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env['res.users'].search_count([('hotel_id', '=', record.id)])
    def action_view_employee(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Employees'),
            'res_model': 'res.users',
            'view_mode': 'kanban,list,form',
            'target': 'current',
            'context': {'default_hotel_id': self.id},
            'domain': [('hotel_id','=',self.id)],
        }

    @api.depends('room_ids')
    def _compute_room_count(self):
        for record in self:
            record.room_count = self.env['hotel.room'].search_count([('hotel_id', '=', record.id)])
    def action_view_room(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Rooms'),
            'res_model': 'hotel.room',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_hotel_id': self.id},
            'domain': [('hotel_id','=',self.id)],
        }

    @api.depends('payment_ids')
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = self.env['hotel.payment'].search_count([('hotel_id', '=', record.id)])
    def action_view_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'hotel.payment',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_hotel_id': self.id},
            'domain': [('hotel_id', '=', self.id)],
        }

    @api.depends('guest_ids')
    def _compute_guest_count(self):
        for record in self:
            record.guest_count = self.env['hotel.guest'].search_count([('hotel_id', '=', record.id)])
    def action_view_guest(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Guests'),
            'res_model': 'hotel.guest',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_hotel_id': self.id},
            'domain': [('hotel_id', '=', self.id)],
        }

class HotelBankAccount(models.Model):
    _name = 'hotel.bank.account'
    _description = 'Hotel Bank Account'

    name = fields.Char(string="Bank Name", required=True, tracking=True)
    acc_type = fields.Selection([('current','Current'),('saving','Saving')], string="Account Type", tracking=True, required=True)
    acc_no = fields.Char(string="Account Number", required=True, tracking=True)
    acc_balance = fields.Float(string="Account Balance", tracking=True)
    hotel_id = fields.Many2one('res.company', string='Hotel', required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")