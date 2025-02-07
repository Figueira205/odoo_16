from odoo import models, fields

class CrmLeadProductoSubtipo(models.Model):
    _name = 'crm.lead.producto_subtipo'
    _description = 'Subtipo de Producto'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    name = fields.Char(string='Nombre', required=True)
    producto_tipo_id = fields.Many2one('crm.lead.producto_tipo', string='Tipo de Producto', required=True)