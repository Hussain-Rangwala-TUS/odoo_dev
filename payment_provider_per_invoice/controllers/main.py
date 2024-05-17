import logging
import pprint

from odoo import http
from odoo.http import request
from odoo.addons.payment.controllers import portal as payment_portal

_logger = logging.getLogger(__name__)


class PaymentPortal(payment_portal.PaymentPortal):
    def _get_custom_rendering_context_values(self, **kwargs):
        """Override of `payment` to add the invoice id in the custom rendering context values.

        :param int invoice_id: The invoice for which a payment id made, as an `account.move` id.
        :param dict kwargs: Optional data. This parameter is not used here.
        :return: The extended rendering context values.
        :rtype: dict
        """
        rendering_context_values = super()._get_custom_rendering_context_values(
            **kwargs
        )
        if rendering_context_values and rendering_context_values.get("invoice_id"):
            invoice_sudo = (
                request.env["account.move"]
                .sudo()
                .browse(rendering_context_values.get("invoice_id"))
            )
            if invoice_sudo.state != "cancel":
                partner_sudo = request.env.user.partner_id  # env.user is always sudoed
                providers_sudo = (
                    request.env["payment.provider"]
                    .sudo()
                    ._get_compatible_providers(
                        request.env.company.id,
                        partner_sudo.id,
                        0.0,  # There is no amount to pay with validation transactions.
                        force_tokenization=True,
                        is_validation=True,
                    )
                )

                if invoice_sudo.payment_provider_ids:
                    rendering_context_values["providers"] = providers_sudo.filtered(
                        lambda p: p.id in invoice_sudo.payment_provider_ids.ids
                    )

        return rendering_context_values
