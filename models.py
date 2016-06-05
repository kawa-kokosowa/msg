import datetime
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Post(Base):
    """A submission to the site, just some text,
    a timestamp, an associated user, and an ID.

    """

    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.datetime.utcnow)
    text = sqlalchemy.Column(sqlalchemy.String())

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Post #%s>' % self.id

    def to_dict(self):
        return {'id': self.id,
                'text': self.text,
                'created': self.created.isoformat("T") + 'Z'}
