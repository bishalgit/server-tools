# -*- coding: utf-8 -*-

import werkzeug
from odoo import http
from odoo.addons import oauth_provider
from odoo.addons.web.controllers.main import ensure_db
from ..oauth2.validator import JWTOdooValidator

class OAuth2ProviderController(
        oauth_provider.controllers.controllers.OAuth2ProviderController):
    jwtOdooValidator = JWTOdooValidator();
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

    @http.route(
        '/oauth2/test', type='http', auth='none', methods=['GET'])
    def test(self, access_token=None, *args, **kwargs):
        """ Returns the public key of the requested client """
        ensure_db()

        token, payload = self.jwtOdooValidator.authenticate_jwt(http.request.httprequest)
        if not token:
            return self._json_response(
                data={'error': 'invalid_or_expired_token'}, status=401)

        data = {'check': 'helloworld!'}
        return self._json_response(data=data)
