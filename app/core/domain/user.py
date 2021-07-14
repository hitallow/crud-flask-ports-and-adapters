from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GenderEnum(str, Enum):
    MALE: str = "Male"
    FEMALE: str = "Female"
    NOTSPECIFIED: str = "Not specified"


@dataclass
class User:
    id: Optional[int]
    username: str
    name: str
    last_name: str
    profile_image_url: str
    bio: str
    email: str
    gender: str

    def __init__(self,
                 username: str,
                 name: str,
                 email: str,
                 profile_image_url: str = '',
                 last_name: str = '',
                 bio: str = '',
                 gender: str = GenderEnum.NOTSPECIFIED,
                 id: int = None,
                 ) -> None:
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.profile_image_url = profile_image_url
        self.last_name = last_name
        self.bio = bio
        self.gender = gender

    def __repr__(self) -> str:
        return '<User %r>' % (self.name)


@dataclass
class SaveUserDTO:
    username: str
    name: str
    email: str

    def __init__(self, username: str, name: str, email: str) -> None:
        self.name = name
        self.username = username
        self.email = email

    def validate(self) -> None:
        required_fields = ['username', 'name', 'email']

        for field in required_fields:
            if not hasattr(self, field):
                raise 'Missing required field: %s' % (field)


@dataclass
class GithubUser:
    name: str
    profileImageUrl: str
    email: str
    bio: str
    login: str
    gender: str

    def __repr__(self) -> str:
        return '<GithubUser %r>' % (self.name)


@dataclass
class GithubUserInformations:
    total_followers: int
    total_public_repositories: int
    total_following: int
    profile_url: int
