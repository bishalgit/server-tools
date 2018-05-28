# -*- coding: utf-8 -*-

import werkzeug
from odoo import http
from odoo.addons import oauth_provider
from odoo.addons.web.controllers.main import ensure_db


class OAuth2ProviderController(
        oauth_provider.controllers.controllers.OAuth2ProviderController):
    @http.route(
        '/oauth2/public_key', type='http', auth='none', methods=['GET'])
    def public_key(self, client_id=None, *args, **kwargs):
        """ Returns the public key of the requested client """
        ensure_db()

        client = http.request.env['oauth.provider.client'].sudo().search([
            ('identifier', '=', client_id),
        ])
        return werkzeug.wrappers.BaseResponse(
            client.jwt_public_key or '', status=200)
