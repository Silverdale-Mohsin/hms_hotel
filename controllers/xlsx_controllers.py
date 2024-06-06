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

        output = BytesIO() # Store the workbook in memory
        workbook = xlsxwriter.Workbook(output, {'in_memory': True}) # Creates workbook
        worksheet = workbook.add_worksheet('Payment Report') # Creates worksheet in workbook

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1, 'align': 'center'})
        data_format = workbook.add_format({'align': 'center'})

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 18)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 18)
        worksheet.set_column('J:J', 15)
        worksheet.set_column('K:K', 15)

        headers = ['Receipt #', 'Guest', 'Reservation', 'Amount', 'Method', 'Date', 'Card Type', 'Card #', 'Card Expiry', 'Successful', 'State']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        row = 1
        for record in payment_records:
            worksheet.write(row, 0, record.receipt_number, data_format)
            worksheet.write(row, 1, record.guest_id.name, data_format)
            worksheet.write(row, 2, record.reservation_id.reservation_ref, data_format)
            worksheet.write(row, 3, f"{record.amount} $", data_format)
            worksheet.write(row, 4, record.payment_method.replace('_', ' ').capitalize(), data_format)
            worksheet.write(row, 5, str(record.payment_date), data_format)
            worksheet.write(row, 6, record.card_id.card_type, data_format)
            worksheet.write(row, 7, record.card_number, data_format)
            worksheet.write(row, 8, str(record.card_expiry), data_format)
            worksheet.write(row, 9, record.is_successful, data_format)
            worksheet.write(row, 10, record.state.capitalize(), data_format)
            row += 1
        workbook.close()

        output.seek(0)
        file_data = output.read() # Output buffer is reset to the beginning using seek(0) to prepare for reading.
        output.close()
        # The content of the output buffer is read into file_data.
        response = request.make_response(
            file_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Payment_Report.xlsx;')
            ]
        )
        return response