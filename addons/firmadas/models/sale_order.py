from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.message_post(body=f'El presupuesto {order.name} ha sido confirmado automáticamente.')
        return res