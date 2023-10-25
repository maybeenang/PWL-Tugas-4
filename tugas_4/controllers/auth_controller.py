from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.request import Request
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models import User
import json
from pyramid.httpexceptions import HTTPUnauthorized


@view_config(route_name="login", request_method="POST", renderer="json")
def login(request: Request):
    try:
        username = request.json_body["username"]
        password = request.json_body["password"]
    except:
        return Response(
            content_type="application/json",
            charset="UTF-8",
            status=400,
            body=json.dumps({"error": "username or password is empty"}),
        )

    query = request.dbsession.query(User).filter(User.name == username)

    if query.count() == 0:
        return Response(
            content_type="application/json",
            charset="UTF-8",
            status=401,
            body=json.dumps({"error": "username not found"}),
        )

    user = query.first()

    if User.check_password(pw=password, self=user) is False:
        return Response(
            content_type="application/json",
            charset="UTF-8",
            status=401,
            body=json.dumps({"error": "wrong password"}),
        )

    token = request.create_jwt_token(
        user.id,
        role=user.role,
    )

    return Response(
        content_type="application/json",
        charset="UTF-8",
        body=json.dumps(
            {
                "message": "Berhasil Login",
                "data": {
                    "access-token": token,
                },
            }
        ),
    )
