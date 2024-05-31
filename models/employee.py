# -*- coding: utf-8 -*-
import re
from datetime import date, datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HotelEmployee(models.Model):
    _inherit = "res.users"

    is_employee = fields.Boolean(string="is_Employee", default=True)
    hotel_id = fields.Many2one('res.company', string='Hotel')
    employee_ref = fields.Char(string="Reference", default='New')
    gender_new = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    phone_no = fields.Char(string="Phone Number")
    emergency_contact_name = fields.Char(string="Name")
    emergency_contact_number = fields.Char(string="Phone Number")
    date_of_birth = fields.Date(string="Date of Birth")
    registration_date = fields.Date(string="Registration Date", default=fields.Date.context_today)
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday')
    cnic_no = fields.Char(string="CNIC Number")
    tag_ids = fields.Many2many('hotel.tag', string="Tags")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital Status")
    emp_department_id = fields.Many2one('hotel.department', string='Department')
    emp_position_id = fields.Many2one('hotel.position', string='Position')
    role = fields.Selection([('admin', 'Admin'), ('manager', 'Manager'), ('employee', 'Employee')], string="Role")

    @api.model
    def create(self, vals):
        vals['employee_ref'] = self.env['ir.sequence'].next_by_code('res.users')
        return super(HotelEmployee, self).create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = datetime.today().date()
        for record in self:
            if record.date_of_birth:
                age = today.year - record.date_of_birth.year - (
                        (today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
                record.age = age
            else:
                record.age = 0

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

class HotelDeptartment(models.Model):
    _name = 'hotel.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Department'

    name = fields.Char(string="Department Name")
    description = fields.Text(string="Description")
    head_of_department_id = fields.Many2one('res.users', string='Head of Department')
    hotel_id = fields.Many2one(related="head_of_department_id.hotel_id", string='Hotel', store=True)
    created_date = fields.Date(string="Created Date", default=fields.Date.context_today)
    position_ids = fields.One2many('hotel.position', 'department_id', string='Positions')

class HotelPosition(models.Model):
    _name = 'hotel.position'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hotel Position'

    name = fields.Char(string="Position Title")
    description = fields.Text(string="Description")
    department_id = fields.Many2one('hotel.department', string='Department')
    salary_range = fields.Char(string='Salary Range')
    created_date = fields.Date(string="Created Date", default=fields.Date.context_today)