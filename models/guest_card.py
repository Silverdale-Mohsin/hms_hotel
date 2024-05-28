# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class HotelGuestCard(models.Model):
    _name = 'hotel.guest.card'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Guest Card'
    _rec_name = 'card_type'

    guest_id = fields.Many2one('hotel.guest', string="Guest", tracking=True, required=True)
    guest_ref = fields.Char(related='guest_id.guest_ref', string="Guest Reference", tracking=True)
    card_type = fields.Selection([('visa','Visa'),('master','Master'),('union_pay','UnionPay'),('pay_pak','PayPak')], string="Card Type", tracking=True, required=True)
    card_number = fields.Char(string="Card Number", tracking=True, required=True)
    card_expiry = fields.Date(string="Card Expiry", tracking=True, required=True)

    @api.model
    def create(self, vals):
        self._validate_card_number(vals.get('card_type'), vals.get('card_number'))
        self._validate_card_expiry(vals.get('card_expiry'))
        return super(HotelGuestCard, self).create(vals)

    def write(self, vals):
        if 'card_type' in vals or 'card_number' in vals:
            card_type = vals.get('card_type', self.card_type)
            card_number = vals.get('card_number', self.card_number)
            self._validate_card_number(card_type, card_number)
        if 'card_expiry' in vals:
            self._validate_card_expiry(vals.get('card_expiry'))
        return super(HotelGuestCard, self).write(vals)

    def _validate_card_number(self, card_type, card_number):
        patterns = {
            'master': r"^(5[1-5][0-9]{14}|2(2[2-9][0-9]{2}|[3-6][0-9]{3}|7[01][0-9]{2}|720)[0-9]{12})$",
            'visa': r"^4[0-9]{12}(?:[0-9]{3})?$",
            'union_pay': r"^62[0-9]{14,17}$",
            'pay_pak': r"^81[0-9]{14}$"
        }
        if card_type and card_number:
            pattern = patterns.get(card_type)
            if pattern and not re.match(pattern, card_number):
                raise ValidationError(_("The card number is invalid for the selected card type."))

    def _validate_card_expiry(self, card_expiry):
        if card_expiry:
            card_expiry_date = fields.Date.from_string(card_expiry)
            today = fields.Date.context_today(self)
            max_expiry_date = today + timedelta(days=5 * 365)
            if card_expiry_date > max_expiry_date:
                raise ValidationError(_("Expiry date can't be more than 5 years."))

    # MASTER
    # 5123456789012345 , 5256789012345678 , 2221001234567890 , 2720998765432100
    # VISA
    # 4123456789012 , 4123456789012345 , 4916123456789012 , 4024007139271310
    # UNIONPAY
    # 6212345678901234 , 621234567890123456 , 6212345678901234567 , 6223456789012345678
    # PAYPAK
    # 8134567890123456 , 8112345678901234 , 8123456789012345 , 8145678901234567