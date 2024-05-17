from odoo import fields, models, api
from odoo.osv import expression


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_provider = fields.Boolean(
        string='Restrict Payment Provider',
        config_parameter='payment_provider_per_invoice.payment_provider',
        related='company_id.payment_provider',
    )


    def _getProviderDomain(self):
        # Compute the base domain for compatible providers.
        domain = [
            # "&",
            ("state", "in", ["enabled", "test"]),
            # ("company_id", "=", self.company_id.id),
        ]

        # Handle partner country.
        if self.partner_id.country_id:
            # The partner country must either not be set or be supported.
            domain = expression.AND(
                [
                    domain,
                    [
                        "|",
                        ("available_country_ids", "=", False),
                        (
                            "available_country_ids",
                            "in",
                            [self.partner_id.country_id.id],
                        ),
                    ],
                ]
            )
        return domain

    payment_provider_ids = fields.Many2many(
        "payment.provider",
        string="Payment Providers",
        help="On portal payment only display the payment providers that are selected with this invoice",
        domain=_getProviderDomain,
    )
