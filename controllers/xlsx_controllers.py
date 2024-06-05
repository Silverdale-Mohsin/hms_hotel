from io import BytesIO
import xlsxwriter
from odoo.http import request, Response
from odoo import http

class PaymentReport(http.Controller):
    @http.route('/payment/report', type='http', auth='user')
    def get_employee_report(self, payment_ids=None, **kwargs):
        if payment_ids:
            payment_ids = list(map(int, payment_ids.split(',')))
            payment_records = request.env['hotel.payment'].browse(payment_ids)
        else:
            payment_records = request.env['hotel.payment'].search([])

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Payment Report')

        bold = workbook.add_format({'bold': True})
        headers = ['Receipt #', 'Guest', 'Reservation', 'Amount', 'Method', 'Date', 'Card Type', 'Card #', 'Card Expiry', 'Successful', 'State']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold)
        row = 1
        for record in payment_records:
            worksheet.write(row, 0, record.receipt_number)
            worksheet.write(row, 1, record.guest_id.name)
            worksheet.write(row, 2, record.reservation_id.reservation_ref)
            worksheet.write(row, 3, record.amount)
            worksheet.write(row, 4, record.payment_method)
            worksheet.write(row, 5, str(record.payment_date))
            worksheet.write(row, 6, record.card_id.card_type)
            worksheet.write(row, 7, record.card_number)
            worksheet.write(row, 8, str(record.card_expiry))
            worksheet.write(row, 9, record.is_successful)
            worksheet.write(row, 10, record.state)
            row += 1
        workbook.close()

        output.seek(0)
        file_data = output.read()
        output.close()

        response = request.make_response(
            file_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Payment_Report.xlsx;')
            ]
        )
        return response