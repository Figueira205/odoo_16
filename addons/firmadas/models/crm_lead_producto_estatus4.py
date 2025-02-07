from odoo import models, fields

class CrmLeadProductoEstatus4(models.Model):
    _name = 'crm.lead.producto_estatus4'
    _description = 'Estatus 4'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    name = fields.Char(string='Nombre', required=True)
    producto_estatus3_id = fields.Many2one('crm.lead.productoestatus3', string='Estatus 3', required=False)