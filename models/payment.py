# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelPayment(models.Model):
    _name = 'hotel.payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Payment'
    _rec_name = 'reservation_id'

    receipt_number = fields.Char(string='Receipt Number', default='New', tracking=True)
    guest_id = fields.Many2one('hotel.guest', string="Guest", tracking=True, required=True)
    reservation_id = fields.Many2one('hotel.reservation', string="Reservation", tracking=True, required=True)
    card_id = fields.Many2one('hotel.guest.card', string="Card Type", tracking=True)
    card_count = fields.Integer(related='guest_id.card_count', string="Card", tracking=True)
    card_number = fields.Char(string="Card Number", tracking=True)
    card_expiry = fields.Date(string="Card Expiry", tracking=True)
    amount = fields.Monetary(related="reservation_id.price_subtotal", string="Amount", tracking=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")
    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today, tracking=True)
    payment_method = fields.Selection([('cash','Cash'),('credit_card','Credit Card')], string="Payment Method", tracking=True, required=True)
    is_successful = fields.Boolean(string="Payment Successful", tracking=True)
    state = fields.Selection([('draft','Draft'),('successful','Successful')], default="draft", string="Status", required=True, tracking=True)
    hotel_id = fields.Many2one('res.company', string='Hotel', tracking=True, required=True)

    @api.model
    def create(self, vals):
        if vals.get('receipt_number', _('New')) == _('New'):
            current_datetime = datetime.now()
            sequence = f"REC{current_datetime.strftime('%d%m%Y%H%M%S')}"
            vals['receipt_number'] = sequence
        return super(HotelPayment, self).create(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'successful':
                raise ValidationError(_("Can only delete Payments in DRAFT state"))
        return super(HotelPayment, self).unlink()

    @api.onchange('card_id', 'card_number')
    def _onchange_card_fields(self):
        if self.card_id:
            self.card_number = False
            self.card_expiry = False
        if self.card_id and self.card_number:
            cards = self.env['hotel.guest.card'].search([('guest_id', '=', self.guest_id.id), ('card_type', '=', self.card_id.card_type)])
            for card in cards:
                if self.card_number == card.card_number:
                    self.card_expiry = card.card_expiry
                    break
            else:
                self.card_expiry = False

    def action_payment_successful(self):
        for record in self:
            if not record.hotel_id.bank_account_ids:
                raise ValidationError(_("The selected hotel does not have a bank account."))
            bank_account = record.hotel_id.bank_account_ids[0]

            if record.payment_method == 'cash':
                return self._process_cash_payment(record, bank_account)
            elif record.payment_method == 'credit_card':
                return self._process_credit_card_payment(record, bank_account)

    def _process_cash_payment(self, record, bank_account):
        record.is_successful = True
        record.state = 'successful'
        bank_account.acc_balance += record.amount
        if record.reservation_id:
            record.reservation_id.state = 'confirm'
            self._send_same_room_notification(record.reservation_id)
            if record.reservation_id.room_id:
                record.reservation_id.room_id.is_available = False
        return {'effect': {'fadeout': 'slow', 'message': 'Payment Successful!', 'type': 'rainbow_man'}}

    def _process_credit_card_payment(self, record, bank_account):
        if record.card_id and record.card_number:
            cards = self.env['hotel.guest.card'].search([('guest_id', '=', record.guest_id.id),('card_type', '=', record.card_id.card_type)])
            for card in cards:
                if record.card_number == card.card_number:
                    record.card_expiry = card.card_expiry
                    record.is_successful = True
                    record.state = 'successful'
                    bank_account.acc_balance += record.amount
                    if record.reservation_id:
                        record.reservation_id.state = 'confirm'
                        self._send_same_room_notification(record.reservation_id)
                        if record.reservation_id.room_id:
                            record.reservation_id.room_id.is_available = False
                    return {'effect': {'fadeout': 'slow', 'message': 'Payment Successful!', 'type': 'rainbow_man'}}

    def _send_same_room_notification(self, reservation):
        pending_reservations = self.env['hotel.reservation'].search([('room_id', '=', reservation.room_id.id), ('state', '=', 'pending'), ('id', '!=', reservation.id)])
        template = self.env.ref('hms_hotel.reservation_confirmed_same_room_mail_template')
        for res in pending_reservations:
            if res.guest_id.email:
                template.send_mail(res.id, force_send=True)

    def action_view_cards(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cards'),
            'res_model': 'hotel.guest.card',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_guest_id': self.guest_id},
            'domain': [('guest_id', '=', self.guest_id)],
        }