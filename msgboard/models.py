import datetime
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import (generate_password_hash,
                               check_password_hash)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.datetime.utcnow)
    username = sqlalchemy.Column(sqlalchemy.String(30), unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String())
    bio = sqlalchemy.Column(sqlalchemy.String())

    def __init__(self, username, password, bio=None):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.bio = bio

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Return a dictionary representation of this
        user, which keys are in jsonStyle.

        """

        return {'username': self.username,
                'bio': self.bio,
                'id': self.id,
                'created': self.created.isoformat("T") + 'Z'}


class Post(Base):
    """A submission to the site, just some text,
    a timestamp, an associated user, and an ID.

    """

    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(User.id))
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.datetime.utcnow)
    text = sqlalchemy.Column(sqlalchemy.String())

    user = sqlalchemy.orm.relationship('User', foreign_keys='Post.user_id',
                                       lazy='subquery')

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return '<Post #%s>' % self.id

    def to_dict(self):
        """Return a dictionary representation of this
        user, which keys are in jsonStyle.

        """

        return {'id': self.id,
                'text': self.text,
                'user': self.user.to_dict(),
                'created': self.created.isoformat("T") + 'Z'}
