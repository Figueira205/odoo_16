from odoo import models, fields

class CrmLeadProductoEstatus1(models.Model):
    _name = 'crm.lead.producto_estatus1'
    _description = 'Estatus 1'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    name = fields.Char(string='Nombre', required=True)
    producto_subtipo_id = fields.Many2one('crm.lead.producto_subtipo', string='Tipo de Subproducto', required=False)