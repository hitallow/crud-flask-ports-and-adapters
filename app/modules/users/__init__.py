from flask import Flask

from .controllers.save_user import save_new_user
from .controllers.update_user import update_user
from .controllers.get_user_profile import get_profile_user
from .controllers.list_user_by_email import list_with_email
from .controllers.list_user_by_username import list_user_by_username
from .controllers.list_user_by_name import list_user_by_name
from .controllers.list_all_users import list_all_users
from .controllers.register_with_github import register_with_github


def register_user_routes(app: Flask):
    # inser user
    app.add_url_rule('/users', view_func=save_new_user, methods=['POST'])

    #  inser user by github
    app.add_url_rule(
        '/users/register/github', view_func=register_with_github, methods=['POST'])

    # list user by user email
    app.add_url_rule('/users/email/<string:user_email>',
                     view_func=list_with_email, methods=['GET'])

    # list user by username
    app.add_url_rule('/users/username/<string:user_username>',
                     view_func=list_user_by_username, methods=['GET'])

    # list all users
    app.add_url_rule('/users', view_func=list_all_users, methods=['GET'])

    # load user profile
    app.add_url_rule('/users/<int:user_id>/profile',
                     view_func=get_profile_user, methods=['GET'])

    # search user by name
    app.add_url_rule('/users/search/<string:like_name>',
                     view_func=list_user_by_name, methods=['GET'])
