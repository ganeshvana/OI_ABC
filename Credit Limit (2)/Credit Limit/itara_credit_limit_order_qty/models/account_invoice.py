from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        
        invoice_total = 0
        payment_total = 0
        exceed_amount = 0
        customer_inv = self.env["account.invoice"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
        for inv in customer_inv:
            invoice_total+= inv.amount_total
        customer_payment = self.env["account.payment"].search([('partner_id','=', self.partner_id.id), ('payment_type', '=','inbound'),('state','in',['posted','reconciled'])])
        for pay in customer_payment:
            payment_total+= pay.amount
        sale = self.env['sale.order'].search([('name','=',self.origin)])
        if payment_total > invoice_total:
            print ("else")
            res = super(Invoice, self).action_invoice_open()
            return res
        elif invoice_total > payment_total:
            exceed_amount = (invoice_total + sale.amount_total) - payment_total
        
        if exceed_amount > self.partner_id.credit_limit:
            print ("ggggggggggggggggg")
            raise UserError(_('Credit limit exceeded for this customer'))
        else:
            res = super(Invoice, self).action_invoice_open()
            return res
