from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = 'account.invoice'

    override_credit_limit = fields.Boolean("Override Credit Limit")

    @api.multi
    def action_invoice_open(self):
        if self.type == 'out_invoice':
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
            ordered_quantity = all(line.product_id.invoice_policy == 'order' for line in self.invoice_line_ids)
            if payment_total > invoice_total:
                print ("else")
                to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                    raise UserError(_("Invoice must be in draft state in order to validate it."))
                if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                    raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                to_open_invoices.action_date_assign()
                to_open_invoices.action_move_create()
                return to_open_invoices.invoice_validate()
            elif invoice_total > payment_total:
                exceed_amount = (invoice_total + sale.amount_total) - payment_total
            print ("ordered_quantity",ordered_quantity)
            if ordered_quantity:
                if exceed_amount > self.partner_id.credit_limit:
                    print (self.override_credit_limit, "self.override_credit_limit")
                    if self.override_credit_limit:
                        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                            raise UserError(_("Invoice must be in draft state in order to validate it."))
                        if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                        to_open_invoices.action_date_assign()
                        to_open_invoices.action_move_create()
                        return to_open_invoices.invoice_validate()
                    else:
                        print ("ddddddddddddd")
                        raise UserError(_('Credit limit exceeded for this customer'))
                else:
                    to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                    if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                        raise UserError(_("Invoice must be in draft state in order to validate it."))
                    if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                        raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                    to_open_invoices.action_date_assign()
                    to_open_invoices.action_move_create()
                    return to_open_invoices.invoice_validate()
            else:
                raise UserError(_('Select all products with Ordered quantities Invoicing policy'))
        else:
            to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
            if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                raise UserError(_("Invoice must be in draft state in order to validate it."))
            if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
            to_open_invoices.action_date_assign()
            to_open_invoices.action_move_create()
            return to_open_invoices.invoice_validate()