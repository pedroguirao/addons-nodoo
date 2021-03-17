from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class Set(models.Model):
    _name = 'set'
    _description = 'Set'

    name = fields.Char('Reference')
    set_name = fields.Char('Name')
    set_description = fields.Text('Description')
    department_id = fields.Many2one('set.department')
    sector_id = fields.Many2one('set.sector')
    quality_id = fields.Many2one('set.quality')
    brand_id = fields.Many2one('product.brand')
    serie_id = fields.Many2one('set.serie')
    type_id = fields.Many2one('set.type')
    line_ids = fields.One2many('set.lines', 'set_id')

