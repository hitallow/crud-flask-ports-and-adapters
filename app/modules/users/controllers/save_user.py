from typing import Tuple
from flask import request, jsonify

from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import SaveUserDTO, SaveUserUsecase


def save_new_user() -> Tuple[dict, int]:

    data = request.get_json()

    user_data = SaveUserDTO(
        email=data['email'], name=data['name'], username=data['username']
    )

    try:
        user_data.validate()
    except Exception as e:
        return jsonify({'message': e}), 404

    user_repository = UserRepository()

    usecase = SaveUserUsecase(
        save_user_interface_port=user_repository, load_user_port=user_repository)

    try:
        result, status_code = usecase.execute(userToSave=user_data)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
