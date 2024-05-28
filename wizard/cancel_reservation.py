# -*- coding: utf-8 -*-
from datetime import date
import datetime
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelCancelReservationWizard(models.TransientModel):
    _name = 'hotel.cancel.reservation.wizard'
    _description = 'Hotel Cancel Reservation Wizard'

    @api.model
    def default_get(self, fields):
        res = super(HotelCancelReservationWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['reservation_id'] = self.env.context.get('active_id')
        return res

    guest_id = fields.Many2one('hotel.guest', string="Guest")
    reservation_id = fields.Many2one('hotel.reservation', string="Reservation")
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('hms_hotel.cancel_days')
        print("cancel_day",cancel_day)
        allowed_date = self.reservation_id.check_in_date - relativedelta.relativedelta(days=int(cancel_day))
        print("allowed_date",allowed_date)
        if cancel_day != 0 and allowed_date < date.today():
            raise ValidationError(_("Sorry! Cancellation is not allowed for this booking"))
        self.reservation_id.state = 'cancel'

        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'cancel.appointment.wizard',
        #     'target': 'new',
        #     'res_id': self.id,
        # }

        # if self.reservation_id.reservation_date == fields.Date.today():
        #     raise ValidationError(_("Sorry! Cancellation is not allowed on the same day of booking"))
        # else:
        #     self.reservation_id.state = 'cancel'

        return{
        'type': 'ir.actions.client',
        'tag': 'reload',
    }