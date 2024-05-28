# -*- coding: utf-8 -*-
import re
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelEmployee(models.Model):
    _inherit = "hr.employee"

    is_employee = fields.Boolean(string="is_Employee", default=True, tracking=True)
    hotel_id = fields.Many2one('res.company', string='Hotels', required=True, tracking=True)