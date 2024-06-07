# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelTags(models.Model):
    _name = 'hotel.tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Tags'

    sequence = fields.Integer(string="Sequence", readonly=True, store=True, tracking=True, group_operator=False)
    name = fields.Char(string="Name", required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    type = fields.Selection([('tag_guest','Guest'),('tag_reservation','Reservation'),('tag_room','Room'),('tag_employee','Employee')], string="Type", required=True, tracking=True)
    color = fields.Integer(string="Color", required=True, tracking=True, group_operator=False)

    @api.model
    def create(self, vals):
        if 'sequence' not in vals:  # If sequence is not explicitly provided
            vals['sequence'] = self.search_count([]) + 1  # Increment based on existing records count
        return super(HotelTags, self).create(vals)

    def write(self, vals):
        res = super(HotelTags, self).write(vals)
        if 'sequence' in vals:  # If sequence is provided in the update, ignore
            return res
        for record in self:
            if not record.sequence:
                record.sequence = record.search_count([]) + 1  # Recalculate sequence
        return res

    def unlink(self):
        res = super(HotelTags, self).unlink()
        # Recalculate sequence for all remaining records
        sequence = 1
        for record in self.search([], order="sequence"):
            record.sequence = sequence
            sequence += 1
        return res

    _sql_constraints = [('unique_tag_name','unique (name,active)','Name must be unique')]