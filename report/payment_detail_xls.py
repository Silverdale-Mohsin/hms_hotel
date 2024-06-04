# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64
import io

class PaymentDetailXlsx(models.AbstractModel):
    _name = 'report.hms_hotel.report_xls_payment_detail'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, payments):
        sheet = workbook.add_worksheet('Payment Details')
        heading_format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        heading_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'red'})
        date_format = workbook.add_format({'num_format': 'd mmmm yyyy', 'align': 'center'})
        data_format = workbook.add_format({'align': 'center'})
        row = 2
        col = 0
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 18)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 18)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 15)
        for obj in payments:
            sheet.merge_range(0, 0, 0, 10, "Payment Details", heading_format_1)
            sheet.write(1, 0, "Receipt #", heading_format)
            sheet.write(1, 1, "Guest", heading_format)
            sheet.write(1, 2, "Reservation", heading_format)
            sheet.write(1, 3, "Amount", heading_format)
            sheet.write(1, 4, "Payment Method", heading_format)
            sheet.write(1, 5, "Payment Date", heading_format)
            sheet.write(1, 6, "Card Type", heading_format)
            sheet.write(1, 7, "Card #", heading_format)
            sheet.write(1, 8, "Card Expiry", heading_format)
            sheet.write(1, 9, "Successful", heading_format)
            sheet.write(1, 10, "State", heading_format)

            sheet.write(row, col, obj.receipt_number, data_format)
            col += 1
            sheet.write(row, col, obj.guest_id.name, data_format)
            col += 1
            sheet.write(row, col, obj.reservation_id.reservation_ref, data_format)
            col += 1
            sheet.write(row, col, f"{obj.amount} $", data_format)
            col += 1
            sheet.write(row, col, obj.payment_method.replace('_', ' ').capitalize(), data_format)
            col += 1
            sheet.write(row, col, obj.payment_date, date_format)
            col += 1
            sheet.write(row, col, obj.card_id.card_type, data_format)
            col += 1
            sheet.write(row, col, obj.card_number, data_format)
            col += 1
            sheet.write(row, col, obj.card_expiry, date_format)
            col += 1
            sheet.write(row, col, obj.is_successful, data_format)
            col += 1
            sheet.write(row, col, obj.state.capitalize(), data_format)

            row += 1
            col = 0

    # if obj.image:
            #     guest_image = io.BytesIO(base64.b64decode(obj.image))
            #     sheet.insert_image(row, col, "image.png", {'image_data': guest_image, 'x_scale': 0.5, 'y_scale': 0.5})
            #     row += 5