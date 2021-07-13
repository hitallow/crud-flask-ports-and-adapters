from flask.json import jsonify
from flask import request

from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import LoadUserByLikeNameUsecase


def list_user_by_name(like_name: str):
    limit = request.args.get('limit', None)
    offset = request.args.get('offset', None)

    usecase = LoadUserByLikeNameUsecase(
        load_user_port=UserRepository()
    )

    try:
        result, status_code = usecase.execute(
            like_name, limit=limit, offset=offset)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
