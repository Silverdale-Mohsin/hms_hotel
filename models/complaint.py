# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelComplaint(models.Model):
    _name = 'hotel.complaint'
    _description = 'Hotel Complaint'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'complaint_no'

    @api.model
    def default_get(self, fields):
        res = super(HotelComplaint, self).default_get(fields)
        if self.env.context.get('active_id'):
            res['guest_id'] = self.env.context.get('active_id')
        return res

    complaint_no = fields.Char(string='Complaint Number', default='New')
    subject = fields.Char(string='Subject', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'),('in_progress', 'In Progress'),('resolved', 'Resolved'),('cancelled', 'Cancelled'),], string='Status', default='draft', required=True)
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    priority = fields.Selection([('normal', 'Normal'),('urgent', 'Urgent'),], string='Priority', default='normal', required=True)
    assigned_to = fields.Many2one('res.users', string='Assigned To', required=True)
    guest_id = fields.Many2one('hotel.guest', string="Guest", required=True)
    hotel_id = fields.Many2one(related='guest_id.hotel_id', string='Hotel', tracking=True)
    guest_ref = fields.Char(related='guest_id.guest_ref', string="Guest Reference", required=True)
    reservation_id = fields.Many2one('hotel.reservation', string="Reservation", required=True)
    tag_ids = fields.Many2many('hotel.tag', string="Tags", tracking=True)

    @api.model
    def create(self, vals):
        vals['complaint_no'] = self.env['ir.sequence'].next_by_code('hotel.complaint')
        complaint = super(HotelComplaint, self).create(vals)
        complaint._complaint_receiving_mail_for_guest()
        complaint._complaint_receiving_mail_for_assigned()
        return complaint

    def _complaint_receiving_mail_for_guest(self):
        template = self.env.ref('hms_hotel.complaint_receiving_template_for_guest')
        for rec in self:
            if rec.guest_id.email:
                template.send_mail(rec.id, force_send=True)

    def _complaint_receiving_mail_for_assigned(self):
        template = self.env.ref('hms_hotel.complaint_receiving_template_for_assigned')
        for rec in self:
            if rec.assigned_to.email:
                template.send_mail(rec.id, force_send=True)

    def _complaint_resolved_mail_for_guest(self):
        template = self.env.ref('hms_hotel.complaint_resolved_template_for_guest')
        for rec in self:
            if rec.guest_id.email:
                template.send_mail(rec.id, force_send=True)

    def action_in_progress(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = 'in_progress'

    def action_resolved(self):
        for rec in self:
            if rec.state == "in_progress":
                rec.state = 'resolved'
                rec._complaint_resolved_mail_for_guest()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Issue Resolved',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        for rec in self:
            if rec.state == "draft" or rec.state == "in_progress":
                rec.state = 'cancelled'