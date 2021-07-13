from typing import Tuple

from app.core.ports.user import GetUserInformationsFromGithubInterfacePort, GetUserMetricsGithubInterfacePort, GetUsersInformationsFromGithubWithUsername, SaveUserPort, LoadUserPort
from app.core.domain.user import SaveUserDTO, User


class SaveUserUsecase:
    save_user_interface_port: SaveUserPort
    load_user_port: LoadUserPort

    def __init__(self,
                 save_user_interface_port: SaveUserPort,
                 load_user_port: LoadUserPort
                 ) -> None:
        self.load_user_port = load_user_port
        self.save_user_interface_port = save_user_interface_port

    def execute(self, userToSave: SaveUserDTO) -> Tuple[dict, int]:
        user = self.load_user_port.load_user_by_email(userToSave.email)
        if user is not None:
            return {'message': 'User with same email saved'}, 404

        user = self.load_user_port.load_user_by_username(userToSave.username)

        if user is not None:
            return {'message': 'User with same name saved'}, 404

        response = self.save_user_interface_port.save(userToSave)

        return {'user': response}, 201


class SaveUserWithGithubUsernameUsecase:
    get_github_informations_port: GetUserInformationsFromGithubInterfacePort
    save_user_interface_port: SaveUserPort
    load_user_port: LoadUserPort
    get_users_from_github_by_username_port: GetUsersInformationsFromGithubWithUsername

    def __init__(self,
                 save_user_interface_port: SaveUserPort,
                 get_github_informations_port: GetUserInformationsFromGithubInterfacePort,
                 load_user_port: LoadUserPort,
                 get_users_from_github_by_username_port: GetUsersInformationsFromGithubWithUsername
                 ) -> None:
        self.load_user_port = load_user_port
        self.save_user_interface_port = save_user_interface_port
        self.get_github_informations_port = get_github_informations_port
        self.get_users_from_github_by_username_port = get_users_from_github_by_username_port

    def execute(self, github_username: str) -> Tuple[dict, int]:

        user = self.load_user_port.load_user_by_username(
            username=github_username)

        if user is not None:
            return {'user': user}, 201

        github_informations = self.get_github_informations_port.load_github_informations(
            username=github_username
        )

        if github_informations is None:
            availible_users = self.get_users_from_github_by_username_port.load_users_by_username(
                username=github_username, limit=50)
            return {'message': 'User not found on github', 'availableUsers': availible_users}, 404

        user = User(
            username=github_informations.login,
            name=github_informations.name,
            last_name='',
            bio=github_informations.bio,
            email=github_informations.email,
            gender=github_informations.gender,
            profile_image_url=github_informations.profileImageUrl)

        response = self.save_user_interface_port.save(user)

        return {'user': response}, 201


class LoadUserProfileUsecase:
    load_user_port: LoadUserPort
    get_user_metrics_port: GetUserMetricsGithubInterfacePort

    def __init__(self, load_user_port: LoadUserPort,
                 get_user_metrics_port: GetUserMetricsGithubInterfacePort
                 ) -> None:
        self.load_user_port = load_user_port
        self.get_user_metrics_port = get_user_metrics_port

    def execute(self, user_id: int) -> Tuple[dict, int]:
        user: User = self.load_user_port.load_user_by_id(id=user_id)

        if user is None:
            return {'message': 'User not found'}, 404

        result = vars(user)

        if hasattr(user, 'username'):
            user_metrics = self.get_user_metrics_port.load_user_metrics(
                user.username)
            if user_metrics is not None:
                result.update(vars(user_metrics))

        return {'user': result}, 200


class LoadUserByEmailUsecase:
    load_user_port: LoadUserPort

    def __init__(self, load_user_port: LoadUserPort) -> None:
        self.load_user_port = load_user_port

    def execute(self, user_email: str) -> Tuple[dict, int]:
        user = self.load_user_port.load_user_by_email(email=user_email)

        if user is None:
            return {'message': 'User not found'}, 404

        return {'user': user}, 200


class LoadUserByUsernameUsecase:
    load_user_port: LoadUserPort

    def __init__(self, load_user_port: LoadUserPort) -> None:
        self.load_user_port = load_user_port

    def execute(self, user_username: str) -> Tuple[dict, int]:
        user = self.load_user_port.load_user_by_username(
            username=user_username)

        if user is None:
            return {'message': 'User not found'}, 404

        return {'user': user}, 200


class LoadUsersUsecase:
    load_user_port: LoadUserPort

    def __init__(self, load_user_port: LoadUserPort) -> None:
        self.load_user_port = load_user_port

    def execute(self, limit=0, offset=0) -> Tuple[dict, int]:
        users = self.load_user_port.load_users(limit=limit, offset=offset)
        return {'users': users}, 200


class LoadUserByLikeNameUsecase:
    load_user_port: LoadUserPort

    def __init__(self, load_user_port: LoadUserPort) -> None:
        self.load_user_port = load_user_port

    def execute(self, like_name: str, limit: int = None, offset: int = None) -> Tuple[dict, int]:
        users = self.load_user_port.load_user_by_like_name(
            like_name=like_name, limit=limit, offset=offset)
        return {'users': users}, 200
