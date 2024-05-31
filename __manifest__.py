# -*- coding: utf-8 -*-
{
    'name': "Hotel Management",
    'summary': """Short (1 phrase/line) summary of the module's purpose, used as subtitle on modules listing or apps.openerp.com""",
    'description': """Long description of module's purpose""",
    'author': "Muhammad Mohsin",
    'website': "http://www.mohsin.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['mail', 'base', 'product', 'hr', 'portal'],
    # always loaded
    'data': [
        # SEQURITY
        'security/ir.model.access.csv',
        'security/security_access_data.xml',
        # DATA
        'data/hotel.tag.csv',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        # WIZARD
        'wizard/cancel_reservation_view.xml',
        # VIEWS
        'views/portal_template.xml',
        'views/menu.xml',
        'views/hotel_view.xml',
        'views/hotel_bank_account_view.xml',
        'views/guest_view.xml',
        'views/guest_card_view.xml',
        'views/reservation_view.xml',
        'views/booking_view.xml',
        'views/tags_view.xml',
        'views/room_view.xml',
        'views/employee_view.xml',
        'views/employee_department_view.xml',
        'views/employee_position_view.xml',
        'views/service_view.xml',
        'views/facility_view.xml',
        'views/feedback_view.xml',
        'views/payment_view.xml',
        'views/settings_views.xml',
        # REPORT
        'report/report.xml',
        'report/guest_detail.xml',
        'report/reservation_detail.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/hms_hotel/static/src/css/hms_hotel.css',
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'sequence': -100,
    'application': True,
}
