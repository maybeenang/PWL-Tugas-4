def includeme(config):
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("user", "/api/v1/users")
    config.add_route("article", "/api/v1/articles")
    config.add_route("login", "/api/v1/login")
    config.add_route("register", "/api/v1/register")
    config.add_route("logout", "/api/v1/logout")
