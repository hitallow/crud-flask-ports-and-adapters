from flask.json import jsonify

from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import LoadUserByEmailUsecase


def list_with_email(user_email: str):
    usecase = LoadUserByEmailUsecase(load_user_port=UserRepository())
    try:
        result, status_code = usecase.execute(user_email=user_email)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
