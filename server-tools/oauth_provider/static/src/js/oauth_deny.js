odoo.define('oauth_provider.OauthDeny', function (require) {
	"use strict";

    var core = require('web.core');
	var Widget = require('web.Widget');
    var rpc = require('web.rpc');

	var OauthDeny = Widget.extend({
		events: {
			'click .oauth_deny': '_deny_request',
		},
		template: 'authorize_deny',
		xmlDependencies: ['/oauth_provider/static/src/xml/authorize.xml'],
		init: function (parent) {
			this._super(parent);
			console.log("init");
		},
		start: function () {
			console.log("start");
			console.log(this.$el.find(".oauth_deny"));
		},
		_deny_request: function () {
		    var self = this;
			console.log("deny");
			rpc.query({
                route: '/oauth2/deny',
                params: { name: "oauth_deny"},
            }).then(function (data) {
                if (data) {
                    if (JSON.parse(data).grant == 400)
                        window.location.replace(JSON.parse(data).redirect_uri);
                    console.log(data);
                }else {
                    console.log("400");
                }
            });
		},

	});

	var oauthDeny = new OauthDeny(this);
	oauthDeny.appendTo(".oauth_provider");

	return OauthDeny;
});