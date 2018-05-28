# -*- coding: utf-8 -*-

from odoo import models, fields


class OAuthProviderRedirectURI(models.Model):
    _name = 'oauth.provider.redirect.uri'
    _description = 'OAuth Provider Redirect URI'

    name = fields.Char(required=True, help='URI of the redirect.')
    sequence = fields.Integer(
        required=True, default=10, help='Order of the redirect URIs.')
    client_id = fields.Many2one(
        comodel_name='oauth.provider.client', string='Client', required=True,
        help='Client allowed to redirect using this URI.')
