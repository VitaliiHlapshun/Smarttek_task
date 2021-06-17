from odoo import models, fields, api


class Demo(models.Model):
    _name = 'demo.demo'
    _description = 'demo.demo'
    _rec_name = 'name_seq'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    customer = fields.Char(string="Customer", required=True)
    done_date = fields.Date(string="Done Date")
    salesperson = fields.Char(string="Salesperson")
    state = fields.Selection([('cancelled', 'Cancelled'), ('done', 'Done'), ('planned', 'Planned')], default='planned',
                             string="Status", track_visibility='onchange')
    crm_lead_id = fields.Many2one("crm.lead", string="Lead", required=True)
    name_seq = fields.Char(string='Demo Order Reference', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('Demo'))


    @api.model
    def default_get(self, fields_list):
        res = super(Demo, self).default_get(fields_list)
        a = self.env['crm.lead'].search([])
        partner = a['partner_id']
        res['customer'] = partner
        return res

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('Demo')) == ('Demo'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('demo.demo.sequence') or ('Demo')
        result = super(Demo, self).create(vals)
        return result
