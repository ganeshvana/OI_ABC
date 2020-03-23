
from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_itara_credit_limit = fields.Boolean(string='Credit Limit - Delivered Quantity')
    module_itara_credit_limit_delivered_qty_override = fields.Boolean(string='Credit Limit - Delivered Quantity(Override)')
    module_itara_credit_limit_order_qty = fields.Boolean(string='Credit Limit - Ordered Quantity')
    module_itara_credit_limit_order_qty_override = fields.Boolean(string='Credit Limit - Ordered Quantity(Override)')