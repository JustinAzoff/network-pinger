"""Pylons middleware initialization"""
from beaker.middleware import CacheMiddleware, SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware

from networkpinger.config.environment import load_environment


def add_auth(app):

    # We need to set up the repoze.who components used by repoze.what for
    # authentication
    from repoze.who.plugins.htpasswd import HTPasswdPlugin, crypt_check
    from repoze.who.plugins.basicauth import BasicAuthPlugin
    htpasswd = HTPasswdPlugin('passwd', crypt_check)
    basicauth = BasicAuthPlugin('Alerts')
    identifiers = [('basicauth', basicauth)]
    authenticators = [('htpasswd', htpasswd)]
    challengers = [('basicauth', basicauth)]
    mdproviders = []

    # We'll use group and permission based exclusively on INI files
    from repoze.what.plugins.ini import INIGroupAdapter
    from repoze.what.plugins.ini import INIPermissionsAdapter

    groups = {'all_groups': INIGroupAdapter('groups.ini')}
    permissions = {'all_perms': INIPermissionsAdapter('permissions.ini')}

    # Finally, we create the repoze.what middleware
    import logging

    from repoze.what.middleware import setup_auth

    middleware = setup_auth(
        app = app,
        group_adapters = groups,
        permission_adapters = permissions, 
        identifiers = identifiers, 
        authenticators = authenticators,
        challengers = challengers, 
        mdproviders = mdproviders, 
        log_level = logging.DEBUG
    )
    return middleware

def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether this application provides a full WSGI stack (by default,
        meaning it handles its own exceptions and errors). Disable
        full_stack when this application is "managed" by another WSGI
        middleware.

    ``static_files``
        Whether this application serves its own static files; disable
        when another web server is responsible for serving them.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).

    """
    # Configure the Pylons environment
    load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp()

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    app = add_auth(app)
    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    return app
