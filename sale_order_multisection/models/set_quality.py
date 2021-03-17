from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetQuality(models.Model):
    _name = 'set.quality'
    _description = 'Quality'

    name = fields.Char('Name')
