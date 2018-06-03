# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import base64
import urllib
import logging

from odoo import http, fields

_logger = logging.getLogger(__name__)

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, hmac
except ImportError:
    _logger.debug('Cannot `import hmac`.')


class APIValidator(object):
    """ API request validator to be used in Odoo

        This will ensure that the request comes from authenticated client
    """

    @staticmethod
    def _verify_client(method, host, path, client_id, body, signature):
        """ Check if the provided access client_id is valid """
        _logger.warning(method)
        _logger.warning(host)
        _logger.warning(path)
        _logger.warning(client_id)
        _logger.warning(body)
        _logger.warning(signature)

        client = http.request.env['oauth.provider.client'].search([
            ('identifier', '=', client_id),
        ])

        if not client:
            return False

        # Prepare parameter/value pairs
        canonical_string = urllib.parse.urlencode({'client_id':base64.urlsafe_b64encode(bytes(client_id,'utf-8')).decode()}) + "&" + urllib.parse.urlencode(body)

        # Prepare message
        message = method + "\n" + host + "\n" + path + "\n" + canonical_string

        # Calculate an an RFC 2104-compliant HMAC with the SHA256 hash algorithm
        algorithm_suffix = client.jwt_algorithm[2:]
        if algorithm_suffix == '256':
            h = hmac.HMAC(bytes(client.jwt_private_key, 'utf-8'), hashes.SHA256(), backend=default_backend())
        elif algorithm_suffix == '384':
            h = hmac.HMAC(bytes(client.jwt_private_key, 'utf-8'), hashes.SHA384(), backend=default_backend())
        else:
            h = hmac.HMAC(bytes(client.jwt_private_key, 'utf-8'), hashes.SHA512(), backend=default_backend())

        _logger.warning("message:" + message)
        # Update byte message into hmac
        h.update(bytes(message, 'utf-8'))
        digest = h.finalize()
        _logger.warning("digest:" + str(digest))
        # Calculate an RFC 2104-compliant HMAC with the SHA256 hash
        # algorithm using the string above with this example secret
        # key: 457967861b296e9e4b5e006784f9219e8f6da355fdc9e28d7707b01ec58ad1d1.
        # For more information about this step, see documentation and code
        # samples for your programming language.
        #
        # URL encode the plus (+) and equal (=) characters in the signature:
        created_signature = urllib.parse.quote_plus(base64.urlsafe_b64encode(digest).decode(encoding="utf-8"))

        _logger.warning("new sign:" + created_signature)
        # # Verify the signature
        if created_signature != signature:
            return False

        return client

    @staticmethod
    def _get_request_information(request):
        """ Extract auth string from request headers """
        auth = request.headers.get('Authorization', ' ')
        auth_type, auth_string = auth.split(' ', 1)
        if auth_type != 'Key':
            return ''

        if request.method == "GET":
            return request.method, request.host, request.path, auth_string, request.args

        return request.method, request.host, request.path, auth_string, request.form

    @staticmethod
    def _extract_key_info(auth_string):
        """ Extract header, client_id, and signature from jwt """
        client_id, signature = auth_string.split(':')
        return (base64.urlsafe_b64decode(client_id)).decode(encoding="utf-8"), signature

    @staticmethod
    def authenticate_jwt(request, *args, **kwargs):
        """ Authenticate the jwt """
        method, host, path, auth_string, body = APIValidator._get_request_information(request)
        client_id, signature = APIValidator._extract_key_info(auth_string)

        # start validating the request
        client = APIValidator._verify_client(method, host, path, client_id, body, signature)
        if not client:
            return False

        return client

