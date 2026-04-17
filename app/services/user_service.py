from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password
from app.utils.validators import require_text


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, username: str, password: str, role: str):
        username = require_text(username, 'usuario')
        password = require_text(password, 'contraseña')
        role = require_text(role, 'rol').lower()
        if role not in ('admin', 'cajero'):
            raise ValueError('Rol inválido. Use admin o cajero.')
        password_hash = hash_password(password)
        return self.repository.create(username, password_hash, role)

    def list_users(self):
        return self.repository.list_users()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def update_user(self, user_id: int, role: str | None = None, password: str | None = None):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado.')
        update_params = {}
        if role:
            role = require_text(role, 'rol').lower()
            if role not in ('admin', 'cajero'):
                raise ValueError('Rol inválido. Use admin o cajero.')
            if user.role == 'admin' and role != 'admin':
                admin_count = self.repository.count_admins()
                if admin_count <= 1:
                    raise ValueError('No se puede degradar al último administrador.')
            update_params['role'] = role
        if password:
            password_hash = hash_password(require_text(password, 'contraseña'))
            update_params['password_hash'] = password_hash
        return self.repository.update(user, **update_params)

    def delete_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado.')
        if user.role == 'admin':
            admin_count = self.repository.count_admins()
            if admin_count <= 1:
                raise ValueError('No se puede eliminar al último administrador.')
        self.repository.delete(user)
