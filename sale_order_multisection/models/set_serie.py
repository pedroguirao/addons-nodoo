from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetSerie(models.Model):
    _name = 'set.serie'
    _description = 'Serie'

    name = fields.Char('Name')
