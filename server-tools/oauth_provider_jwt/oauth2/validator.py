# -*- coding: utf-8 -*-

import base64
import logging
from odoo import http, fields
from odoo.addons.oauth_provider.oauth2.validator import OdooValidator

_logger = logging.getLogger(__name__)

try:
    import jwt
except ImportError:
    _logger.debug('Cannot `import jwt`.')

try:
    import oauthlib
    from oauthlib import oauth2
except ImportError:
    _logger.debug('Cannot `import oauthlib`.')


class JWTOdooValidator(OdooValidator):
    """ OAuth2 JWT validator to be used in Odoo

    This is an implementation of oauthlib's RequestValidator interface
    https://github.com/idan/oauthlib/oauthlib/oauth2/rfc6749/request_validator.py
    """

    @staticmethod
    def _get_request_information(request):
        """ Retrieve needed arguments for oauthlib methods """
        uri = request.base_url
        http_method = request.method
        body = oauthlib.common.urlencode(
            request.values.items())
        headers = request.headers

        return uri, http_method, body, headers

    @staticmethod
    def _check_access_token(access_token, request):
        """ Check if the provided access token is valid """
        token = http.request.env['oauth.provider.token'].search([
            ('token', '=', access_token),
        ])
        if not token:
            return False

        oauth2_server = token.client_id.get_oauth2_server()
        # Retrieve needed arguments for oauthlib methods
        uri, http_method, body, headers = JWTOdooValidator._get_request_information(request)

        # Validate request information
        valid, oauthlib_request = oauth2_server.verify_request(
            uri, http_method=http_method, body=body, headers=headers)

        if valid:
            return token

        return False

    @staticmethod
    def _extract_jwt(request):
        """ Extract auth string from request headers """
        auth = request.headers.get('Authorization', ' ')
        auth_type, auth_string = auth.split(' ', 1)
        if auth_type != 'Bearer':
            return ''

        return auth_string

    @staticmethod
    def _extract_jwt_info(auth_string):
        """ Extract header, payload, and signature from jwt """
        header, payload, signature = auth_string.split('.')
        return jwt.get_unverified_header(auth_string), jwt.decode(auth_string, verify=False), signature

    @staticmethod
    def authenticate_jwt(request, *args, **kwargs):
        """ Authenticate the jwt """
        auth_string = JWTOdooValidator._extract_jwt(request)
        unverified_header, unverified_payload, signature = JWTOdooValidator._extract_jwt_info(auth_string)

        token = JWTOdooValidator._check_access_token(auth_string, request)
        if not token:
            return False, False

        # Get client public key
        payload = jwt.decode(auth_string, token.client_id.jwt_public_key,
                             algorithms=unverified_header['alg'], audience=token.client_id.identifier)
        if payload:
            return token, payload
        else:
            return False, False
