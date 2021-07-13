from flask import request, jsonify
from typing import Tuple

from app.core.usecase.user import SaveUserWithGithubUsernameUsecase
from app.database.repositories.user_repository import UserRepository
from app.modules.users.services.github_api import LoadGithubInformations


def register_with_github() -> Tuple[dict, int]:

    data = request.get_json()

    if not 'username' in data:
        return {'message': 'Missing required field: username'}, 400

    try:
        user_repository = UserRepository()
        usecase = SaveUserWithGithubUsernameUsecase(
            load_user_port=user_repository,
            save_user_interface_port=user_repository,
            get_github_informations_port=LoadGithubInformations()
        )

        response, status_code = usecase.execute(data['username'])

        data = jsonify(response)

        return data, status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
