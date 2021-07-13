from flask.json import jsonify

from app.modules.users.services.github_api import LoadGithubInformations
from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import LoadUserProfileUsecase


def get_profile_user(user_id: int):

    usecase = LoadUserProfileUsecase(load_user_port=UserRepository(),
                                     get_user_metrics_port=LoadGithubInformations()
                                     )

    try:
        result, status_code = usecase.execute(user_id=user_id)
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
