from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SetDepartment(models.Model):
    _name = 'set.department'
    _description = 'Department'

    name = fields.Char('Name')
