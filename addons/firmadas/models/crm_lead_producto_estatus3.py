from odoo import models, fields

class CrmLeadProductoEstatus3(models.Model):
    _name = 'crm.lead.producto_estatus3'
    _description = 'Estatus 3'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    name = fields.Char(string='Nombre', required=True)
    producto_estatus2_id = fields.Many2one('crm.lead.producto_estatus2', string='Estatus 2', required=False)