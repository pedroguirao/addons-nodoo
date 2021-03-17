from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetLine(models.Model):
    _name = 'set.lines'
    _description = 'Set Lines'

    name = fields.Char('Reference')
    quantity = fields.Float('Quantity')
    set_id = fields.Many2one('set')
    product_id = fields.Many2one('product.product')

