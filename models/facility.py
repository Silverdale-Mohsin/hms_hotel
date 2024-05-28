# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelFacility(models.Model):
    _name = 'hotel.facility'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Facility'

    name = fields.Char(string="Name", tracking=True, required=True)
    sequence = fields.Integer(string="Sequence", readonly=True, store=True, tracking=True)
    type = fields.Char(string="Type", tracking=True, required=True)
    description = fields.Text(string="Description", tracking=True, required=True)
    location = fields.Char(string="Location", tracking=True, required=True)
    available_hours = fields.Text(string="Available Hours", tracking=True, required=True)
    contact_person = fields.Many2one('res.users', string="Contact Person", tracking=True, required=True)
    contact_number = fields.Char(string="Contact Number", related="contact_person.phone", tracking=True, required=True)
    reservation_fee = fields.Float(string="Reservation Fee", tracking=True, required=True)
    maintenance_required = fields.Boolean(string="Maintenance Required", tracking=True)
    maintenance_reason = fields.Text(string="Reason", tracking=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")
    reservation_ids = fields.One2many('hotel.reservation', 'room_id', string="Reservations")
    hotel_id = fields.Many2one('res.company', string='Hotels', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if 'sequence' not in vals:  # If sequence is not explicitly provided
            vals['sequence'] = self.search_count([]) + 1  # Increment based on existing records count
        return super(HotelFacility, self).create(vals)

    def write(self, vals):
        res = super(HotelFacility, self).write(vals)
        if 'sequence' in vals:  # If sequence is provided in the update, ignore
            return res
        for record in self:
            if not record.sequence:
                record.sequence = record.search_count([]) + 1  # Recalculate sequence
        return res

    def unlink(self):
        res = super(HotelFacility, self).unlink()
        # Recalculate sequence for all remaining records
        sequence = 1
        for record in self.search([], order="sequence"):
            record.sequence = sequence
            sequence += 1
        return res