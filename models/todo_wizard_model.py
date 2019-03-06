from odoo import models, fields, api
from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'To-do Mass Assignment'
    task_ids = fields.Many2many(
        'todo.task',
        string='Tasks')
    new_deadline = fields.Date('Deadline to Set')
    new_user_id = fields.Many2one(
        'res.users',
        string='Responsible to Set')

    @api.model
    def default_get(self, field_names):
        defaults = super(TodoWizard, self).default_get(field_names)
        defaults['task_ids'] = self.env.context['active_ids']
        return defaults

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise excepitons.ValidationError('No data to update!')
        # Logging debug messages
        _logger.debug(
            'Mass update on Todo Tasks %s',
            self.task_ids.ids)
        vals = {}
        if self.new_deadline:
            vals['date_deadline'] = self.new_deadline
        if self.new_user_id:
            vals['user_id'] = self.new_user_id.id
        # Mass write values on all selected tasks
        if vals:
            self.task_ids.write(vals)
        return True
