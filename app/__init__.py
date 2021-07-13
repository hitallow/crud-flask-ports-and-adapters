from flask import Flask
from app.modules.users import register_user_routes


def register_routes(app: Flask):
    app.add_url_rule(
        "/", view_func=lambda: {'message': 'application is working perfectly'})
    register_user_routes(app)
