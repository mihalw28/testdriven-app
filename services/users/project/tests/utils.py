import json

from project import db
from project.api.models import User


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_admin(username, email, password):
    user = User(username=username, email=email, password=password)
    user.admin = True
    db.session.add(user)
    db.session.commit()
    return user


def register_response(self, username, email, password):
    response = self.client.post(
        "/auth/register",
        data=json.dumps(
            {"username": username, "email": email, "password": password}
        ),
        content_type="application/json",
    )
    return response


def login_response(self, email, password):
    response = self.client.post(
        "/auth/login",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )
    return response
