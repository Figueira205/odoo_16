from odoo import models, fields, api

class EmployeeProductivity(models.Model):
    _name = 'hr.productivity'
    _description = 'Registro de Productividad de Empleados'
    
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    date = fields.Date(string='Fecha', default=fields.Date.today, required=True)
    task_count = fields.Integer(string='Número de Tareas', required=True)
    hours_worked = fields.Float(string='Horas Trabajadas', required=True)
    performance_score = fields.Float(string='Puntuación de Desempeño', compute='_compute_performance_score', store=True)
    notes = fields.Text(string='Notas')
    
    @api.depends('task_count', 'hours_worked')
    def _compute_performance_score(self):
        for record in self:
            record.performance_score = (record.task_count / record.hours_worked) if record.hours_worked else 0.0
    
    _sql_constraints = [
        ('positive_hours', 'CHECK(hours_worked >= 0)', 'Las horas trabajadas deben ser un valor positivo.'),
        ('positive_tasks', 'CHECK(task_count >= 0)', 'El número de tareas debe ser un valor positivo.')
    ]

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    productivity_ids = fields.One2many('hr.productivity', 'employee_id', string='Registro de Productividad')