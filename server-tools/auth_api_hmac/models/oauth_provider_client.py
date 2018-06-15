# -*- coding: utf-8 -*-

import os
import hashlib
import logging
from datetime import datetime, timedelta
from odoo import models, api, fields, exceptions, _

_logger = logging.getLogger(__name__)

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, hmac
except ImportError:
    _logger.debug('Cannot `import cryptography`.')


class OAuthProviderClient(models.Model):
    _inherit = 'oauth.provider.client'

    api_signature = fields.Text(
        string='API Signature', compute='_compute_api_signature',
        help='Signature used for the API request validation.')

    api_key = fields.Text(
        string='API Key', help='API key used for signing API requests.')

    api_key_algorithm = fields.Selection(selection=[
        ('HS256', 'HMAC using SHA-256 hash algorithm'),
        ('HS384', 'HMAC using SHA-384 hash algorithm'),
        ('HS512', 'HMAC using SHA-512 hash algorithm'),
    ], string='API signing Algorithm', help='Algorithm used to sign the API requests.')

    @api.multi
    def _compute_api_signature(self):
        """ Compute the api signature associated to the client's private key

        This is only done for symmetric algorithms
        """
        for client in self:
            if client.api_key and \
                    client.api_key_algorithm[:2] == 'HS':
                h = hmac.HMAC(bytes(client.api_key, 'utf-8'), hashes.SHA256(), backend=default_backend())
                h.update(bytes(client.identifier, 'utf-8'))
                client.api_signature = h.finalize()
            else:
                client.api_signature = False

    @api.multi
    def generate_api_key(self):
        """ Generate a private hmac key for HMAC algorithm clients """
        for client in self:
            algorithm_prefix = client.api_key_algorithm[:2]
            algorithm_suffix = client.api_key_algorithm[2:]

            if algorithm_prefix == 'HS':
                if algorithm_suffix == '256':
                    key = hashlib.sha256(os.urandom(32)).hexdigest()
                elif algorithm_suffix == '384':
                    key = hashlib.sha384(os.urandom(48)).hexdigest()
                elif algorithm_suffix == '512':
                    key = hashlib.sha512(os.urandom(64)).hexdigest()
            else:
                raise exceptions.UserError(
                    _('You can only generate private hmac keys for symetric '
                      'algorithms!'))
            client.api_key = key
