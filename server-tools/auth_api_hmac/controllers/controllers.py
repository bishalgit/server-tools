# -*- coding: utf-8 -*-

import werkzeug
import json
import logging

from odoo import http
from odoo.addons import oauth_provider
from odoo.addons.web.controllers.main import ensure_db
from ..auth.validator import APIValidator

_logger = logging.getLogger(__name__)


class OAuth2ProviderController(
        oauth_provider.controllers.controllers.OAuth2ProviderController):
    @http.route(
            '/oauth2/get_tags', type='http', auth='none', methods=['GET'])
    def test(self, *args, **kwargs):
        """ Returns the public key of the requested client """
        ensure_db()

        _logger.warning("**********")
        _logger.warning(str(http.request.httprequest.args))
        _logger.warning(str(http.request.httprequest.base_url))
        _logger.warning(str(http.request.httprequest.charset))
        _logger.warning(str(http.request.httprequest.cookies))
        _logger.warning(str(http.request.httprequest.data))
        _logger.warning(str(http.request.httprequest.dict_storage_class))
        _logger.warning(str(http.request.httprequest.files))
        _logger.warning(str(http.request.httprequest.form))
        _logger.warning(str(http.request.httprequest.full_path))
        _logger.warning(str(http.request.httprequest.headers))
        _logger.warning(str(http.request.httprequest.host))
        _logger.warning(str(http.request.httprequest.host_url))
        _logger.warning(str(http.request.httprequest.method))
        _logger.warning(str(http.request.httprequest.path))
        _logger.warning(str(http.request.httprequest.query_string))
        _logger.warning(str(http.request.httprequest.remote_addr))
        _logger.warning(str(http.request.httprequest.url))
        _logger.warning(str(http.request.httprequest.url_root))
        _logger.warning(str(http.request.httprequest.values))
        _logger.warning("**********")
        # _logger.warning(str(http.request.httprequest.body))

        client = APIValidator.authenticate_api(http.request.httprequest)
        if not client:
            return self._json_response(
                data={'error': 'invalid_or_expired_token'}, status=401)

        data = {"client_id": client.identifier}
        return self._json_response(data=data)
