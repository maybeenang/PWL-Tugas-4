from sqlalchemy import Column, Integer, Text

from .meta import Base


class Article(Base):
    """The SQLAlchemy declarative model class for a User object."""

    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
