# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Room'
    _rec_name = 'room_no'

    room_no = fields.Char(string="Room Number", tracking=True, required=True)
    type = fields.Selection([('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')], string="Type", tracking=True, required=True)
    price_per_day = fields.Float(string="Price (Per Day)", tracking=True, required=True)
    capacity = fields.Integer(string="Capacity", tracking=True, required=True)
    floor = fields.Integer(string="Floor", tracking=True, required=True)
    view_type = fields.Selection([('sea_view', 'Sea View'), ('city_view', 'City View'), ('garden_view', 'Garden View')], string="View Type", tracking=True, required=True)
    is_smoking_allowed = fields.Boolean(string="Smoking Allowed", tracking=True)
    is_available = fields.Boolean(string="Available", default=True, tracking=True)
    maintenance_required = fields.Boolean(string="Maintenance Required", tracking=True)
    maintenance_reason = fields.Text(string="Reason", tracking=True)
    state = fields.Selection([('clean','Clean'),('dirty','Dirty'),('in_progress','In Progress')], default="clean", string="Status", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', related="hotel_id.currency_id")
    reservation_ids = fields.One2many('hotel.reservation', 'room_id', string="Reservations")
    tag_ids = fields.Many2many('hotel.tag', string="Tags", tracking=True)
    hotel_id = fields.Many2one('res.company', string='Hotels', required=True, tracking=True)
    same_room_reserve = fields.Integer(string='Room Reserve Count', default=0, tracking=True)

    def action_clean(self):
        for rec in self:
            rec.state = 'clean'

    def action_dirty(self):
        for rec in self:
            if rec.state == 'clean':
                rec.state = 'dirty'

    def action_in_progress(self):
        for rec in self:
            if rec.state == 'dirty':
                rec.state = 'in_progress'

    # _sql_constraints = [('unique_room_no','unique (room_no)','Room number must be unique')]