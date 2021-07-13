from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import create_engine


class DBConnection:
    _connection_url: str

    def get_engine(self) -> Engine:
        return create_engine(self._connection_url)

    def __init__(self) -> None:
        self._connection_url = 'sqlite:///./teste.db'

    def __enter__(self):
        session = scoped_session(
            sessionmaker(autocommit=False, bind=self.get_engine())
        )
        self.session = session
        return self

    def __exit__(self, *args, **kwargs) -> bool:
        if self.session is not None:
            self.session.close()
        return False
