from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    nombre = fields.Char(string='Nombre')
    apellido1 = fields.Char(string='Apellido 1')
    apellido2 = fields.Char(string='Apellido 2')

    @api.onchange('nombre', 'apellido1', 'apellido2')
    def _compute_full_name(self):
        for record in self:
            nombres = filter(None, [record.nombre, record.apellido1, record.apellido2])
            record.name = " ".join(nombres) 