from flask.json import jsonify
from flask import request

from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import LoadUsersUsecase


def list_all_users():
    limit = request.args.get('limit', None)
    offset = request.args.get('offset', None)
    usecase = LoadUsersUsecase(load_user_port=UserRepository())

    try:
        result, status_code = usecase.execute(limit=limit, offset=offset)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
