from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request
from ..models import User
import json


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


@view_config(route_name="register", request_method="POST", renderer="json")
def register(request: Request):
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

    if query.count() > 0:
        return Response(
            content_type="application/json",
            charset="UTF-8",
            status=401,
            body=json.dumps({"error": "username already exist"}),
        )

    user = User(name=username, role="user")
    user.set_password(pw=password)
    request.dbsession.add(user)
    request.dbsession.flush()

    return Response(
        content_type="application/json",
        charset="UTF-8",
        body=json.dumps({"message": "success"}),
    )


@view_config(route_name="logout", request_method="GET", renderer="json")
def logout(request: Request):
    return Response(
        content_type="application/json",
        charset="UTF-8",
        body=json.dumps({"message": "success"}),
    )
