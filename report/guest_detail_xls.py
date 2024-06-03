# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64
import io

class GuestDetailXlsx(models.AbstractModel):
    _name = 'report.hms_hotel.report_xls_guest_detail'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, guests):
        # sheet = workbook.add_worksheet('Guests Detail')
        # bold = workbook.add_format({'bold': True})
        for obj in guests:
            row = 2
            col = 0
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.set_column('A:A', 13)
            sheet.set_column('B:B', 12)
            sheet.set_column('C:C', 12)
            sheet.set_column('D:D', 17)
            sheet.set_column('E:E', 10)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 13)
            sheet.set_column('H:H', 13)
            sheet.set_column('I:I', 10)
            sheet.set_column('J:J', 20)
            # bold = workbook.add_format({'bold': True})
            heading_format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
            heading_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'red'})
            date_format = workbook.add_format({'num_format': 'd mmmm yyyy', 'align': 'center'})
            data_format = workbook.add_format({'align': 'center'})

            sheet.merge_range(0, 0, 0, 9, "Guest Details", heading_format_1)

            sheet.write(1, 0, "Name", heading_format)
            sheet.write(1, 1, "Reference", heading_format)
            sheet.write(1, 2, "Gender", heading_format)
            sheet.write(1, 3, "DOB", heading_format)
            sheet.write(1, 4, "Age", heading_format)
            sheet.write(1, 5, "Email", heading_format)
            sheet.write(1, 6, "Phone", heading_format)
            sheet.write(1, 7, "Nationality", heading_format)
            sheet.write(1, 8, "Cards", heading_format)
            sheet.write(1, 9, "Reservations", heading_format)

            sheet.write(row, col, obj.name, data_format)
            col += 1
            sheet.write(row, col, obj.guest_ref, data_format)
            col += 1
            sheet.write(row, col, obj.gender.capitalize(), data_format)
            col += 1
            sheet.write(row, col, obj.date_of_birth, date_format)
            col += 1
            sheet.write(row, col, obj.age, data_format)
            col += 1
            sheet.write(row, col, obj.email, data_format)
            col += 1
            sheet.write(row, col, obj.phone_no, data_format)
            col += 1
            sheet.write(row, col, obj.nationality.capitalize(), data_format)
            col += 1
            sheet.write(row, col, obj.card_count, data_format)
            col += 1
            sheet.write(row, col, obj.reservation_count, data_format)

            row = 6
            col = 0
            for res in obj.reservation_ids:
                sheet.merge_range(4, 0, 4, 9, "Reservation Details", heading_format_1)

                sheet.write(5, 0, "Reference", heading_format)
                sheet.write(5, 1, "Room No.", heading_format)
                sheet.write(5, 2, "Room Type", heading_format)
                sheet.write(5, 3, "Reservation Date", heading_format)
                sheet.write(5, 4, "Duration", heading_format)
                sheet.write(5, 5, "Check_In", heading_format)
                sheet.write(5, 6, "Check_Out", heading_format)
                sheet.write(5, 7, "Price", heading_format)
                sheet.write(5, 8, "Status", heading_format)
                sheet.write(5, 9, "Receipt No.", heading_format)

                sheet.write(row, col, res.reservation_ref, data_format)
                col += 1
                sheet.write(row, col, res.room_id.room_no, data_format)
                col += 1
                sheet.write(row, col, res.room_type, data_format)
                col += 1
                sheet.write(row, col, res.reservation_date, date_format)
                col += 1
                sheet.write(row, col, res.duration, data_format)
                col += 1
                sheet.write(row, col, res.check_in_date, date_format)
                col += 1
                sheet.write(row, col, res.check_out_date, date_format)
                col += 1
                sheet.write(row, col, f"{res.price_subtotal} $", data_format)
                col += 1
                sheet.write(row, col, res.state.capitalize(), data_format)
                col += 1
                sheet.write(row, col, res.receipt_number, data_format)

                row += 1
                col = 0

            # if obj.image:
            #     guest_image = io.BytesIO(base64.b64decode(obj.image))
            #     sheet.insert_image(row, col, "image.png", {'image_data': guest_image, 'x_scale': 0.5, 'y_scale': 0.5})
            #     row += 5