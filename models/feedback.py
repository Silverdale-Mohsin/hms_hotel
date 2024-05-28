# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelFeedback(models.Model):
    _name = 'hotel.feedback'
    _description = 'Hotel Feedback'
    _rec_name = 'guest_id'

    @api.model
    def default_get(self, fields):
        res = super(HotelFeedback, self).default_get(fields)
        if self.env.context.get('active_id'):
            res['guest_id'] = self.env.context.get('active_id')
        return res

    guest_id = fields.Many2one('hotel.guest', string="Guest", required=True)
    guest_ref = fields.Char(related='guest_id.guest_ref', string="Guest Reference", required=True)
    reservation_id = fields.Many2one('hotel.reservation', string="Reservation", required=True)
    rating = fields.Selection([('default','Default'),('worst','Worst'),('bad','Bad'),('normal','Normal'),('good','Good'),('best','Best')], string='Rating', required=True)
    comment = fields.Text(string="Comments", required=True)
    feedback_date = fields.Date(string="Feedback Date", default=fields.Date.context_today)
    response_from_hotel = fields.Text(string="Response")
    response_date = fields.Date(string="Response Date")

    _sql_constraints = [('unique_feedback','unique (reservation_id)','Only one feedback for each reservation')]