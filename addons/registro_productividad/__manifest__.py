# -*- coding: utf-8 -*-
{
    'name': 'Registro de Productividad',
    'version': '1.0',
    'summary': 'Registro de productividad de empleados',
    'description': 'Módulo para registrar métricas de productividad de empleados',
    'author': 'Tu Nombre',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_productivity_views.xml',
        'reports/hr_productivity_reports.xml'
    ],
    'installable': True,
    'application': True,
}