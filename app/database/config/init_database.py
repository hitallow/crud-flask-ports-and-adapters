from .db_connection import DBConnection
from .db_base import Base


def init_database():
    # import all tables
    import app.database.tables
    with DBConnection() as connection:
        Base.metadata.create_all(bind=connection.get_engine())
        connection.session.close()