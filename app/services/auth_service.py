from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password
from app.utils.logger import get_logger
from app.utils.validators import require_text

logger = get_logger(__name__)


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def login(self, username: str, password: str) -> dict:
        username = require_text(username, 'usuario')
        password = require_text(password, 'contraseña')
        user = self.repository.find_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            logger.warning('Intento de acceso fallido para usuario: %s', username)
            raise ValueError('Usuario o contraseña incorrectos.')
        logger.info('Usuario autenticado: %s', username)
        return {'id': user.id, 'username': user.username, 'role': user.role}
