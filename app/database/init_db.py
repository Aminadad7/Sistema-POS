from sqlalchemy.exc import IntegrityError
from app.database.session import engine, SessionLocal
from app.models import Base
from app.models.user import User
from app.models.category import Category
from app.utils.security import hash_password
from app.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_database() -> None:
    Base.metadata.create_all(engine)
    session = SessionLocal()

    try:
        admin = User(username='admin', role='admin', password_hash=hash_password('admin123'))
        session.add(admin)
        session.add_all([
            Category(name='General'),
            Category(name='Alimentos'),
            Category(name='Higiene'),
        ])
        session.commit()
        logger.info('Base de datos inicializada y usuario admin creado.')
    except IntegrityError:
        session.rollback()
        logger.warning('La base de datos ya contiene datos. No se creó el usuario por defecto.')
    finally:
        session.close()
