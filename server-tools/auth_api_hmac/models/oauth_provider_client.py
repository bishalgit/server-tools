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

    @api.multi
    def _compute_api_signature(self):
        """ Compute the api signature associated to the client's private key

        This is only done for symmetric algorithms
        """
        for client in self:
            if client.jwt_private_key and \
                    client.jwt_algorithm[:2] == 'HS':
                h = hmac.HMAC(bytes(client.jwt_private_key, 'utf-8'), hashes.SHA256(), backend=default_backend())
                h.update(bytes(client.identifier, 'utf-8'))
                client.api_signature = h.finalize()
            else:
                client.api_signature = False
