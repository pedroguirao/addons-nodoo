from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderSets(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _get_lines_count(self):
        results = self.env['sale.order.line'].read_group(
            [('order_id', 'in', self.ids), ('display_type', '=', 'line_section')], 'order_id', 'order_id')
        self.set_lines_count = len(results)

    set_lines_count = fields.Integer('Lines', compute=_get_lines_count, stored=False)

    @api.multi
    def action_view_sets(self):
        action = self.env.ref(
            'sale_order_multisection.action_view_set_lines').read()[0]
        return action
