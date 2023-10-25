import json
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from ..models import User


@view_defaults(route_name="user")
class UserView:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            query = self.request.dbsession.query(User)
            res = query.all()
        except DBAPIError:
            return Response(
                content_type="text/plain",
                body="Error",
                status=500,
            )
        return Response(
            content_type="application/json",
            charset="UTF-8",
            body=json.dumps({"data": [dict(id=row.id, name=row.name) for row in res]}),
        )

    @view_config(request_method="POST")
    def post(self):
        try:
            query = self.request.dbsession.query(User)
            res = query.all()
        except DBAPIError:
            return Response(
                content_type="text/plain",
                body="Error",
                status=500,
            )
        return Response(
            content_type="application/json",
            charset="UTF-8",
            body=json.dumps({"data": [dict(id=row.id, name=row.name) for row in res]}),
        )
