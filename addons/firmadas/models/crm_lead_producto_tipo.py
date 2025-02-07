from odoo import models, fields

class CrmLeadProductoTipo(models.Model):
    _name = 'crm.lead.producto_tipo'
    _description = 'Tipo de Producto'
    _auto = True  # Evita que la tabla se elimine al desinstalar el módulo
    _register = True  # Marca el modelo como manual para evitar eliminación

    name = fields.Char(string='Nombre', required=True)