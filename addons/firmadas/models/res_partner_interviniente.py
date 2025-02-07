from odoo import models, fields

class ResPartnerInterviniente(models.Model):
    _name = 'res.partner.interviniente'
    _description = 'Intervinientes'

    partner_id = fields.Many2one('res.partner', string="Interviniente", required=True)
    
    tipo = fields.Selection([
        ('lawyer', 'Abogado'),
        ('notary', 'Notario'),
        ('client', 'Banco')
    ], string="Tipo", required=True)

    def name_get(self):
        """Personaliza la representación de los intervinientes."""
        result = []
        for record in self:
            name = f"{record.partner_id.name} ({dict(self._fields['tipo'].selection).get(record.tipo)})"
            result.append((record.id, name))
        return result