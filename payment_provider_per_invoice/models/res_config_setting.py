from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'


    payment_provider = fields.Boolean(
        string='Restrict Payment Provider',
    )

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_provider = fields.Boolean(
        string='Restrict Payment Provider',
        config_parameter='payment_provider_per_invoice.payment_provider',
        related='company_id.payment_provider',
        readonly=False,
    )