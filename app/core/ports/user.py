from abc import abstractclassmethod

from app.core.domain.user import GithubUser, GithubUserInformations, User, SaveUserDTO
from typing import List, Optional, Union


class LoadUserPort:
    @abstractclassmethod
    def load_user_by_username(self, username: str) -> Optional[User]:
        raise Exception('Not implemented method')

    @abstractclassmethod
    def load_user_by_email(self, email: str) -> Optional[User]:
        raise Exception('Not implemented method')

    @abstractclassmethod
    def load_user_by_id(self, id: int) -> Optional[User]:
        raise Exception('Not implemented method')

    @abstractclassmethod
    def load_users(self, limit=None, offset=None) -> List[User]:
        raise Exception('Not implemented method')

    @abstractclassmethod
    def load_user_by_like_name(self, like_name: str, limit: int = None, offset: int = None) -> List[User]:
        raise Exception('Not implemented method')


class SaveUserPort:
    @abstractclassmethod
    def save(self, user: Union[SaveUserDTO, User]) -> dict:
        raise Exception('Not implemented method save on SaveNewUserPort')


class GetUserInformationsFromGithubInterfacePort:
    @abstractclassmethod
    def load_github_informations(self, username: str) -> Optional[GithubUser]:
        raise Exception('Not implemented method : load_github_informations')


class GetUserMetricsGithubInterfacePort:
    @abstractclassmethod
    def load_user_metrics(self, user_login: str) -> Optional[GithubUserInformations]:
        raise Exception('Not implemented method : load_user_metrics')


class GetUsersInformationsFromGithubWithUsername:
    @abstractclassmethod
    def load_users_by_username(self, username: str, limit: int = 50) -> List[GithubUser]:
        raise Exception('Not implemented method : load_users_by_username')
