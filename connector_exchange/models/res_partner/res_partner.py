# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    exchange_bind_ids = fields.One2many(
        comodel_name='exchange.res.partner',
        inverse_name='openerp_id',
        string="Exchange Bindings",
    )

    @api.multi
    def try_autobind(self, user, backend):
        """
            Try to find a binding with provided backend and user.
            If not found, create a new one.
        """
        for partner in self:
            bindings = partner.exchange_bind_ids.filtered(
                lambda a: a.backend_id == backend and a.user_id == user)
            if not bindings:
                self.env['exchange.res.partner'].sudo().create(
                    {'backend_id': backend.id,
                     'user_id': user.id,
                     'openerp_id': partner.id}
                )
        return True


class ExchangeResPartner(models.Model):
    _name = 'exchange.res.partner'
    _inherit = 'exchange.binding'
    _inherits = {'res.partner': 'openerp_id'}
    _description = 'Exchange Contact'

    openerp_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner',
                                 required=True,
                                 ondelete='cascade')
    created_at = fields.Datetime(string='Created At (on Exchange)',
                                 readonly=True)
    updated_at = fields.Datetime(string='Updated At (on Exchange)',
                                 readonly=True)
