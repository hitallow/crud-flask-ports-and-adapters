from app.database.config.db_connection import DBConnection
from typing import List, Optional, Union

from app.database.tables.user import UserModel
from app.core.domain.user import SaveUserDTO, User
from app.core.ports.user import SaveUserPort, LoadUserPort, UpdateUserPort


class UserRepository(LoadUserPort, SaveUserPort, UpdateUserPort):
    def save(self, user: Union[SaveUserDTO, User]) -> User:
        user_params: User = None

        if isinstance(user, SaveUserDTO):
            user_params = User(
                name=user.name,
                username=user.username,
                email=user.email
            )
        else:
            user_params = user

        with DBConnection() as connection:
            try:
                user_to_save = UserModel(
                    username=user_params.username,
                    name=user_params.name,
                    last_name=user_params.last_name,
                    email=user_params.email,
                    profile_image_url=user_params.profile_image_url,
                    bio=user_params.bio,
                    gender=user_params.gender,
                )

                connection.session.add(user_to_save)
                connection.session.commit()
                connection.session.flush()

                return user_to_save.to_core_model()

            except:
                connection.session.rollback()
                raise Exception('Error on save user')
            finally:
                connection.session.close()

    def load_user_by_email(self, email: str) -> Optional[User]:
        with DBConnection() as connection:
            try:
                user = connection.session.query(
                    UserModel).filter_by(email=email).first()
                if user is not None:
                    return user.to_core_model()
                return None
            except:
                return None
            finally:
                connection.session.close()

    def load_user_by_id(self, id: int) -> Optional[User]:
        with DBConnection() as connection:
            try:
                user = connection.session.query(
                    UserModel).filter_by(id=id).first()
                if user is not None:
                    return user.to_core_model()
                return None
            except:
                return None
            finally:
                connection.session.close()

    def load_user_by_username(self, username: str) -> Optional[User]:
        with DBConnection() as connection:
            try:
                user = connection.session.query(
                    UserModel).filter_by(username=username).first()
                if user is not None:
                    return user.to_core_model()
                return None
            except:
                return None
            finally:
                connection.session.close()

    def load_users(self, limit, offset) -> List[User]:
        with DBConnection() as connection:
            try:
                return connection.session.query(UserModel).limit(limit=limit).offset(offset=offset).all()
            except:
                return []
            finally:
                connection.session.close()

    def load_user_by_like_name(self, like_name: str, limit: int = None, offset: int = None) -> List[User]:
        with DBConnection() as connection:
            try:
                return connection.session.query(UserModel).filter(UserModel.name.ilike(
                    "%s%%" % (like_name)
                )).limit(limit=limit).offset(offset=offset).all()
            except:
                return []
            finally:
                connection.session.close()

    def update_user(self, user_id: int, user: User) -> User:
        with DBConnection() as connection:
            try:
                user_in_database = connection.session.query(
                    UserModel).filter_by(id=user_id).first()

                user_in_database.gender = user.gender
                user_in_database.bio = user.bio
                user_in_database.profile_image_url = user.profile_image_url
                user_in_database.name = user.name

                connection.session.commit()
                return user_in_database.to_core_model()
            except:
                return None
            finally:
                connection.session.close()
