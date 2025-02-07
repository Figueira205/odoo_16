from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _auto = True  # Evita eliminación de la tabla al desinstalar
    _register = True  # Marca el modelo como manual

    importe_firmado = fields.Float(string='Importe Firmado', required=True)
    fecha_firma = fields.Date(string='Fecha de Firma', required=False)
    tipo_contrato = fields.Selection([
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
        ('unico', 'Único')
    ], string='Tipo de Contrato', required=False, default='mensual')
    responsable_firma = fields.Many2one('res.users', string='Responsable de Firma', required=False)
    tiene_factura = fields.Boolean(string='Tiene Factura', default=False, compute='_compute_tiene_factura', store=True)
    factura_id = fields.Many2one('account.move', string='Factura Asociada', readonly=True)
    producto_tipo_id = fields.Many2one('crm.lead.producto_tipo', string='Tipo de Producto', required=True)
    producto_subtipo_id = fields.Many2one('crm.lead.producto_subtipo', string='Subtipo de Producto', domain="[('producto_tipo.id', '=', producto_tipo_id)]", required=True)
    producto_estatus1_id = fields.Many2one('crm.lead.producto_estatus1', string='Estatus 1', domain="[('producto_subtipo.id', '=', producto_subtipo_id)]", required=True)
    producto_estatus2_id = fields.Many2one('crm.lead.producto_estatus2', string='Estatus 2', domain="[('producto_estatus1_id.id', '=', producto_estatus1_id)]", required=False)
    producto_estatus3_id = fields.Many2one('crm.lead.producto_estatus3', string='Estatus 3', domain="[('producto_estatus2_id.id', '=', producto_estatus2_id)]", required=False)
    producto_estatus4_id = fields.Many2one('crm.lead.producto_estatus4', string='Estatus 4', domain="[('producto_estatus3_id.id', '=', producto_estatus3_id)]", required=False)

    gestor_id = fields.Many2one(
        'res.partner', 
        string="Gestor",
        domain="[('id', 'in', available_gestor_ids)]",
    )

    available_gestor_ids = fields.Many2many(
        'res.partner', 
        compute="_compute_available_gestors",
        store=False,
    )

    @api.depends_context('uid')
    def _compute_available_gestors(self):
        """Filtra los contactos que tienen usuario y pertenecen al grupo 'Gestor de Servicio'."""
        group = self.env['res.groups'].search([('name', '=', 'Gestor de Servicio')], limit=1)
        if group:
            users = self.env['res.users'].search([('groups_id', 'in', group.id)])
            self.available_gestor_ids = users.mapped('partner_id')
        else:
            self.available_gestor_ids = self.env['res.partner']

    
    
    intervinientes_ids = fields.Many2many(
        'res.partner.interviniente',
        'crm_lead_interviniente_rel',  # Nombre de la tabla intermedia
        'lead_id',  # Nombre de la columna que referencia a crm.lead
        'interviniente_id',  # Nombre de la columna que referencia a res.partner.interviniente
        string="Intervinientes",
        help="Lista de intervinientes asociados a esta oportunidad"
    )

    cotitulares_ids = fields.Many2many(
        'res.partner',
        'crm_lead_cotitular_rel',  # Nombre de la tabla intermedia
        'lead_id',  # Clave foránea hacia este Lead
        'cotitular_id',  # Clave foránea hacia los Leads relacionados
        string="Cotitulares",
        help="Leads relacionados como cotitulares"
    )

    @api.onchange('producto_tipo_id')
    def _onchange_producto_tipo_id(self):
        self.producto_subtipo_id = False
        self.producto_estatus1_id = False
        self.producto_estatus2_id = False
        self.producto_estatus3_id = False
        self.producto_estatus4_id = False

    @api.onchange('producto_subtipo_id')
    def _onchange_producto_subtipo_id(self):
        self.producto_estatus1_id = False
        self.producto_estatus2_id = False
        self.producto_estatus3_id = False
        self.producto_estatus4_id = False

    @api.onchange('producto_estatus1_id')
    def _onchange_producto_estatus1_id(self):
        self.producto_estatus2_id = False
        self.producto_estatus3_id = False
        self.producto_estatus4_id = False

    @api.onchange('producto_estatus2_id')
    def _onchange_productoestatus2(self):
        self.producto_estatus3_id = False
        self.producto_estatus4_id = False

    @api.onchange('producto_estatus3_id')
    def _onchange_producto_estatus3_id(self):
        self.producto_estatus4_id = False

    @api.depends('factura_id')
    def _compute_tiene_factura(self):
        for lead in self:
            lead.tiene_factura = bool(lead.factura_id)

    def ir_a_factura(self):
        self.ensure_one()
        if self.factura_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Factura',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.factura_id.id,
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        if 'importe_firmado' not in vals or not vals['importe_firmado']:
            vals['importe_firmado'] = vals.get('expected_revenue', 0.0)
        
        lead = super(CrmLead, self).create(vals)
        lead.crear_presupuesto_factura()
        return lead

    def crear_presupuesto_factura(self):
        SaleOrder = self.env['sale.order']
        AccountMove = self.env['account.move']
        
        for lead in self:
            if not lead.partner_id:
                raise models.ValidationError("Debe asignarse un cliente antes de generar la factura.")
            
            # Crear presupuesto
            order = SaleOrder.create({
                'partner_id': lead.partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': self.env.ref('firmadas.product_asesoria').id,
                    'product_uom_qty': 1,
                    'price_unit': lead.importe_firmado,
                })],
            })
            
            # Confirmar pedido automáticamente
            order.action_confirm()
            
            # Crear factura
            invoice = AccountMove.create({
                'partner_id': lead.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_origin': lead.name,
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.env.ref('firmadas.product_asesoria').id,
                    'quantity': 1,
                    'price_unit': lead.importe_firmado,
                })],
            })
            
            lead.with_context(skip_compute=True).write({'factura_id': invoice.id, 'tiene_factura': True})
            lead.message_post(body=f'Se ha generado el presupuesto {order.name} y la factura {invoice.name}')