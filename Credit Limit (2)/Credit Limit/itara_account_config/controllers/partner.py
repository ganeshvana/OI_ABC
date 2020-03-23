import logging

from odoo import http, tools, _
from odoo.http import request

_logger = logging.getLogger(__name__)

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row

class WebsitePartnerLedger(http.Controller):

    @http.route(['/ledger'], type='http', auth="public", website=True)
    def get_ledger(self, **kw):
        partner_id = int(kw.get('partner_id', -1))
        print (partner_id, "partner_id")
        value = {'type': 'ir.actions.client',
                'name': _('Partner Ledger'),
                'tag': 'account_report',
                'options': {'partner_id': partner_id},
                'ignore_session': 'both',
                'context': "{'model':'account.partner.ledger'}"}
        print (value, "v")
        return request.render("itara_account_config.get_ledger", value)