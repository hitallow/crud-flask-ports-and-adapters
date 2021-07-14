from flask.json import jsonify, request

from app.core.domain.user import User
from app.database.repositories.user_repository import UserRepository
from app.core.usecase.user import UpdateUserUsecase


def update_user(user_id: int):
    user_repository = UserRepository()

    usecase = UpdateUserUsecase(
        load_user_port=user_repository,
        update_user_port=user_repository
    )
    request_data: dict = request.get_json()

    user_data = User(
        id=user_id,
        bio=request_data.get('bio', ''),
        name=request_data.get('name', ''),
        email=request_data.get('email', ''),
        username=request_data.get('username', ''),
        gender=request_data.get('gender', 'Not Specified'),
        last_name=request_data.get('last_name'),
        profile_image_url=request_data.get('profile_image_url', '')
    )

    try:
        result, status_code = usecase.execute(
            user_id=user_id,
            user=user_data
        )
        return jsonify(result), status_code
    except:
        return jsonify({'message': 'Internal server error'}), 500
