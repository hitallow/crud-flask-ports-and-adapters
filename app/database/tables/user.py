from sqlalchemy import Column, Integer, String

from app.core.domain.user import User
from app.database.config.db_base import Base


class UserModel(Base, User):
    __tablename__ = "users"

    id = Column('ID', Integer, primary_key=True,
                autoincrement=True, nullable=True)
    username = Column(String(30), unique=True)
    name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=True)
    email = Column(String, unique=True)
    profile_image_url = Column(String(100), nullable=True)
    bio = Column(String(30), nullable=True)
    gender = Column(String(30), default="Not Specified")

    def __repr__(self) -> str:
        return '<UserModel id=%d, name=%s>' % (self.id, self.name)

    def to_core_model(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            profile_image_url=self.profile_image_url,
            bio=self.bio,
            gender=self.gender,
        )
