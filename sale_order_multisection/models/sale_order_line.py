from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    n1 = fields.Char('Capítulo')
    n2 = fields.Char('Subcapítulo')
    n3 = fields.Char('Sección')
    n4 = fields.Char('Subsección')
    n5 = fields.Char('Ud. de obra')

    t_name = fields.Text('Nombre sección', help='Nombre sin código, heredado de la UdO (Set), pero modificable por el usuario')
    set_id = fields.Many2one('set', string="Sets")

    udoline_ids = fields.One2many('sale.order.line', 'udo_id', string='Líneas')

    is_udo = fields.Boolean('Es UdO')
    section_name = fields.Char('Nombre Sección')
    description_noset = fields.Text('Descripción:')
    quantity = fields.Float('Cantidad UdO')
    bysetquantity = fields.Float('Uds/Set')

    is_udo_section = fields.Boolean('Es Unidad de Obra')

    @api.multi
    def _get_used_code(self):
        for record in self:
            usado = ""
            for linea in record.order_id.order_line:
                if ('linea.display_type', '=', 'line_section') and (linea.code):
                    usado += linea.code + "  -  "
            record['used_code'] = usado

    used_code = fields.Char('Código usado', readonly=True,  compute=_get_used_code)

    @api.depends('n1', 'n2', 'n3', 'n4', 'n5')
    def _get_code(self):
        for record in self:
            if record.recalculate_name:
                if record.n5:
                    record[
                        'code'] = record.n1 + "." + record.n2 + "." + record.n3 + "." + record.n4 + "." + record.n5 + " "
                elif record.n4:
                    record['code'] = record.n1 + "." + record.n2 + "." + record.n3 + "." + record.n4 + " "
                elif record.n3:
                    record['code'] = record.n1 + "." + record.n2 + "." + record.n3 + " "
                elif record.n2:
                    record['code'] = record.n1 + "." + record.n2 + " "
                elif record.n1:
                    record['code'] = record.n1 + " "

    code = fields.Char('Código', readonly=True, store=True, compute=_get_code)

    @api.multi
    def _get_description(self):
        for record in self:
            if not record.is_udo_section:
                record['description'] = record.description_noset
            else:
                record['description'] = record.section_description

    description = fields.Text('Descripción', compute=_get_description)

    @api.depends('set_id')
    def _get_section_description(self):
        for record in self:
            if record.is_udo_section and (record.display_type == 'line_section'):
                record['section_description'] = record.set_id.set_description
    section_description = fields.Text('Descripción Sección', store=True, compute=_get_section_description)

    @api.depends('write_date')
    def _get_udo_id(self):
        # Ha de recalcularse siempre, ya que se puede mover por "holder" una sección y esta línea quedar con el mismo ID.
        for record in self:
            udobra = 0
            #
            # Líneas de la oferta, ordenadas por secuencia:
            lineas = self.env['sale.order.line'].search([('id', 'in', record.order_id.order_line.ids)]).sorted(
                key=lambda r: r.sequence)
            #
            # Buscamos la unidad de obra inmediatamente anterior y al pasar por esta línea, la asignamos:
            for li in record.order_id.order_line:
                if li.display_type == 'line_section':
                    udobra = li.id
                if (li.id == record.id) and (record.udo_id.id != udobra):
                    record['udo_id'] = udobra
    udo_id = fields.Many2one('sale.order.line', store=True, readonly=True, compute=_get_udo_id)

    @api.multi
    def _get_section_total(self):
        for record in self:
            subtotal = 0
            nombre = record.internal_name
            # Buscar secciones con ese nombre interno en like:
            secciones = self.env['sale.order.line'].search(
                [('id', 'in', record.order_id.order_line.ids), ('internal_name', 'like', nombre)]).ids
            # Buscar las líneas de esas secciones:
            for li in record.order_id.order_line:
                if li.udo_id.id in secciones:
                    subtotal += li.price_subtotal
            record['section_total'] = subtotal

    section_total = fields.Float('Unit.', readonly=True, compute=_get_section_total)

    @api.multi
    def _get_section_unit_subtotal(self):
        for record in self:
            if record.is_udo_section and (record.quantity > 0):
                record['section_unit_subtotal'] = record.section_subtotal / record.quantity
            else:
                record['section_unit_subtotal'] = 0

    section_unit_subtotal = fields.Float('Unit.', readonly=True, compute=_get_section_unit_subtotal)

    @api.multi
    def _get_section_subtotal(self):
        for record in self:
            subtotal = 0
            for li in record.order_id.order_line:
                if li.udo_id.id == record.udo_id.id:
                    subtotal += li.price_subtotal
            record['section_subtotal'] = subtotal
    section_subtotal = fields.Float('Subtotal Ud. Obra', readonly=True, compute=_get_section_subtotal)

    @api.depends('set_id')
    def _get_set_name(self):
        for record in self:
            if record.set_id and (record.display_type == 'line_section'):
                record['set_name'] = record.set_id.set_name

    set_name = fields.Text('Nombre(Set)', store=True, compute=_get_set_name)

    @api.depends('n1', 'n2', 'n3', 'n4', 'n5', 't_name', 'set_name')
    def _get_recalculate_name(self):
        for record in self:
            if record.display_type == 'line_section':
                if record.n1 and not record.n2 and not record.n3 and not record.n4 and not record.n5:
                    record['recalculate_name'] = True
                elif (record.n1) and (record.n2) and not (record.n3) and not (record.n4) and not (record.n5):
                    record['recalculate_name'] = True
                elif (record.n1) and (record.n2) and (record.n3) and not (record.n4) and not (record.n5):
                    record['recalculate_name'] = True
                elif (record.n1) and (record.n2) and (record.n3) and (record.n4) and not (record.n5):
                    record['recalculate_name'] = True
                elif (record.n1) and (record.n2) and (record.n3) and (record.n4) and (record.n5):
                    record['recalculate_name'] = True

    recalculate_name = fields.Boolean('recalculate_name', store=True, readonly=True, compute=_get_recalculate_name)

    @api.depends('recalculate_name')
    def _get_internal_name(self):
        for record in self:
            if record.n5:
                record[
                    'internal_name'] = "*" + record.n1 + "@" + record.n2 + "#" + record.n3 + "$" + record.n4 + "|" + record.n5 + "!"
            elif record.n4:
                record[
                    'internal_name'] = "*" + record.n1 + "@" + record.n2 + "#" + record.n3 + "$" + record.n4 + "|"
            elif record.n3:
                record['internal_name'] = "*" + record.n1 + "@" + record.n2 + "#" + record.n3 + "$"
            elif record.n2:
                record['internal_name'] = "*" + record.n1 + "@" + record.n2 + "#"
            elif record.n1:
                record['internal_name'] = "*" + record.n1 + "@"
            else:
                record['internal_name'] = "_"

    internal_name = fields.Char('Internal name', store=True, readonly=True, compute=_get_internal_name)

    @api.depends('internal_name')
    def _get_exist(self):
        for record in self:
            if record.n1:
                secciones = self.env['sale.order.line'].search(
                    [('id', 'in', record.order_id.order_line.ids), ('display_type', '=', 'line_section'),
                     ('internal_name', 'like', record.internal_name)])
                if len(secciones.ids) == 0:
                    record['exist'] = 'NUEVA !!!'
                else:
                    nombre = ""
                    for s in secciones:
                        nombre += "=>" + str(s.name) + "\n"
                    record['exist'] = nombre

    exist = fields.Text('Existe:', help="Secciones existentes con el código actual", readonly=True, compute=_get_exist)

    @api.depends('internal_name')
    def _get_level(self):
        for record in self:
            if record.display_type == 'line_section':
                if record.n5:
                    record['level'] = 5
                elif record.n4:
                    record['level'] = 4
                elif record.n3:
                    record['level'] = 3
                elif record.n2:
                    record['level'] = 2
                else:
                    record['level'] = 1

    level = fields.Integer('Nivel:',  readonly=True, store=True, compute=_get_exist)

