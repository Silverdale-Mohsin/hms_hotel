# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelService(models.Model):
    _name = 'hotel.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Service'

    name = fields.Char(string="Name", tracking=True, required=True)
    sequence = fields.Integer(string="Sequence", readonly=True, store=True, tracking=True)
    description = fields.Text(string="Description", tracking=True, required=True)
    cost = fields.Float(string="Cost", tracking=True, required=True)
    is_available = fields.Boolean(string="Available", default=True, tracking=True)
    service_type = fields.Char(string="Service Type", tracking=True, required=True)
    location = fields.Char(string="Location", tracking=True, required=True)
    contact_person = fields.Many2one('res.users',string="Contact Person", tracking=True, required=True)
    duration = fields.Char(string="Duration", tracking=True, required=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")
    reservation_ids = fields.One2many('hotel.reservation', 'room_id', string="Reservations")
    hotel_id = fields.Many2one('res.company', string='Hotels', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if 'sequence' not in vals:  # If sequence is not explicitly provided
            vals['sequence'] = self.search_count([]) + 1  # Increment based on existing records count
        return super(HotelService, self).create(vals)

    def write(self, vals):
        res = super(HotelService, self).write(vals)
        if 'sequence' in vals:  # If sequence is provided in the update, ignore
            return res
        for record in self:
            if not record.sequence:
                record.sequence = record.search_count([]) + 1  # Recalculate sequence
        return res

    def unlink(self):
        res = super(HotelService, self).unlink()
        # Recalculate sequence for all remaining records
        sequence = 1
        for record in self.search([], order="sequence"):
            record.sequence = sequence
            sequence += 1
        return res