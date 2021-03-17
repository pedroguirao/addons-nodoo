from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetSector(models.Model):
    _name = 'set.sector'
    _description = 'Sector'

    name = fields.Char('Name')
