from flask.json import jsonify

from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import LoadUserByUsernameUsecase


def list_user_by_username(user_username: str):

    usecase = LoadUserByUsernameUsecase(load_user_port=UserRepository())
    try:
        result, status_code = usecase.execute(user_username=user_username,)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
