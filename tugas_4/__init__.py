from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from .middlewares import acl

from pyramid.security import ALL_PERMISSIONS

from pyramid.authorization import ACLHelper, Authenticated, Everyone, Allow


class RootACL(object):
    __acl__ = [
        (Allow, "admin", ALL_PERMISSIONS),
        (Allow, "user", "view"),
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include("pyramid_chameleon")
        # Pyramid requires an authorization policy to be active.
        config.set_root_factory(RootACL)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include("pyramid_jwt")
        config.set_jwt_authentication_policy(
            "secret",
            expiration=3600,
            auth_type="Bearer",
            callback=acl.add_role_principals,
        )
        config.include(".routes")
        # config.include(".security")
        config.include(".models")
        config.scan()
    return config.make_wsgi_app()
