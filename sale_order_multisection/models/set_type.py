from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetType(models.Model):
    _name = 'set.type'
    _description = 'Type'

    name = fields.Char('Name')
