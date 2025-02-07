from odoo import models, fields

class CrmLeadProductoEstatus2(models.Model):
    _name = 'crm.lead.producto_estatus2'
    _description = 'Estatus 2'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    name = fields.Char(string='Nombre', required=True)
    producto_estatus1_id = fields.Many2one('crm.lead.producto_estatus1', string='Estatus 1', required=False)