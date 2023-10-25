from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
import json

from .. import models


@view_config(
    route_name="home",
)
def my_view(request):
    return Response(
        content_type="text/plain",
        body="This server is running properly!",
    )


# @view_config(
#     route_name="home",
#     renderer="json",
# )
# def my_view(request):
#     return Response(
#         content_type="application/json",
#         charset="UTF-8",
#         body=json.dumps({"data": [dict(id=row.id, name=row.name) for row in res]}),
#     )


# db_err_msg = """\
# Pyramid is having a problem using your SQL database.  The problem
# might be caused by one of the following things:

# 1.  You may need to initialize your database tables with `alembic`.
#     Check your README.txt for descriptions and try to run it.

# 2.  Your database server may not be running.  Check that the
#     database server referred to by the "sqlalchemy.url" setting in
#     your "development.ini" file is running.

# After you fix the problem, please restart the Pyramid application to
# try it again.
# """
