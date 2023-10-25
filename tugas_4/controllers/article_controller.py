import json
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.request import Request

from sqlalchemy.exc import DBAPIError


from ..models import Article


@view_defaults(route_name="article")
class ArticleView:
    def __init__(self, request):
        self.request: Request = request

    @view_config(request_method="POST", permission="admin")
    def create(self):
        try:
            try:
                title = self.request.json_body["title"]
                content = self.request.json_body["content"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "title or content is empty"}),
                )

            article = Article(title=title, content=content)
            self.request.dbsession.add(article)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )

        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="GET", permission="view")
    def read(self):
        try:
            articles = self.request.dbsession.query(Article).all()
            return Response(
                json={
                    "data": [
                        {
                            "id": article.id,
                            "title": article.title,
                            "content": article.content,
                        }
                        for article in articles
                    ]
                },
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json=json.dumps({"message": "failed"}),
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="PUT", permission="admin")
    def update(self):
        try:
            try:
                id = self.request.json_body["id"]
                title = self.request.json_body["title"]
                content = self.request.json_body["content"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "id, title or content is empty"}),
                )

            article = self.request.dbsession.query(Article).filter_by(id=id).first()

            article.title = title
            article.content = content

            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=201,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="DELETE", permission="admin")
    def delete(self):
        try:
            try:
                id = self.request.json_body["id"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "id is empty"}),
                )

            article = self.request.dbsession.query(Article).filter_by(id=id).first()
            self.request.dbsession.delete(article)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )
