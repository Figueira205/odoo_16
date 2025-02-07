# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Abogado(models.Model):
    _name = "despacho.abogado"
    _description = "Modelo de Abogado"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    edad = fields.Integer(string="Edad", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    points = fields.Float(string="Puntos")
    estado = fields.Selection(
        [
            ("disponible", "Disponible"),
            ("ocupado", "Ocupado"),

        ],
        string="Estado de Disponibilidad",
        default="ocupado",
    )
    
    nivel = fields.Selection(
        [
            ("principiante", "Principiante"),
            ("basico", "Básico"),
            ("avanzado", "Avanzado"),
            ("experto", "Experto"),
        ],
        string="Nivel",
        default="basico",
        required=True,
    )

    # Relación One2many con Cliente
    cliente_ids = fields.One2many("despacho.cliente", "abogado_id", string="Clientes")

    # Relación Many2many con Proceso
    proceso_ids = fields.Many2many(
        comodel_name="despacho.proceso",
        relation="despacho_abogado_proceso_rel",  # Nombre claro de la tabla intermedia
        column1="abogado_id",
        column2="proceso_id",
        string="Procesos",
    )


class Cliente(models.Model):
    _name = "despacho.cliente"
    _description = "Modelo de Cliente"

    name = fields.Char(string="Nombre del Cliente", required=True)

    # Relación Many2one con Abogado
    abogado_id = fields.Many2one("despacho.abogado", string="Abogado", ondelete="set null")

    description = fields.Text(string="Descripción")

    # Relación One2many con Etapa
    etapa_ids = fields.One2many("despacho.etapa", "cliente_id", string="Etapas del Proceso")


class Proceso(models.Model):
    _name = "despacho.proceso"
    _description = "Modelo de Proceso"

    name = fields.Char(string="Tipo de Proceso", required=True)

    # Relación Many2many con Abogado
    abogado_ids = fields.Many2many(
        comodel_name="despacho.abogado",
        relation="despacho_abogado_proceso_rel",
        column1="proceso_id",
        column2="abogado_id",
        string="Abogados",
    )


class Etapa(models.Model):
    _name = "despacho.etapa"
    _description = "Modelo de Etapa del Proceso"

    cliente_id = fields.Many2one("despacho.cliente", string="Cliente", required=True, ondelete="cascade")
    proceso_id = fields.Many2one("despacho.proceso", string="Proceso", required=True, ondelete="cascade")

    etapa = fields.Selection(
        [
            ("bienvenida", "Bienvenida"),
            ("documentacion", "Solicitando Documentación"),
            ("tramite", "En trámite"),
            ("aprobado", "Aprobado"),
            ("finalizado", "Finalizado"),
        ],
        string="Etapa",
        default="bienvenida",
        required=True,
    )
