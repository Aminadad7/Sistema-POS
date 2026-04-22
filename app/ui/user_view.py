from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QSizePolicy,
    QHeaderView,
)
from app.services.user_service import UserService


class UserView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.user_service = UserService()
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Gestión de Usuarios')
        self.title_label.setObjectName('titleLabel')

        self.new_user_username = QLineEdit()
        self.new_user_username.setPlaceholderText('Usuario nuevo')
        self.new_user_password = QLineEdit()
        self.new_user_password.setPlaceholderText('Contraseña')
        self.new_user_password.setEchoMode(QLineEdit.Password)
        self.new_user_role = QComboBox()
        self.new_user_role.addItems(['cajero', 'admin'])

        self.create_user_button = QPushButton('Crear usuario')
        self.create_user_button.clicked.connect(self.create_user)

        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(['ID', 'Usuario', 'Rol'])
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.horizontalHeader().setMinimumSectionSize(90)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_table.setMinimumHeight(560)
        self.user_table.setMinimumWidth(1500)
        self.user_table.setMaximumWidth(2200)
        self.user_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.user_table.setWordWrap(False)
        self.user_table.itemSelectionChanged.connect(self.load_selected_user)

        self.selected_user_label = QLabel('Usuario seleccionado: Ninguno')
        self.selected_user_role = QComboBox()
        self.selected_user_role.addItems(['cajero', 'admin'])
        self.selected_user_password = QLineEdit()
        self.selected_user_password.setPlaceholderText('Nueva contraseña (vacío para no cambiar)')
        self.selected_user_password.setEchoMode(QLineEdit.Password)

        self.update_user_button = QPushButton('Actualizar usuario')
        self.update_user_button.clicked.connect(self.update_user)
        self.delete_user_button = QPushButton('Eliminar usuario')
        self.delete_user_button.clicked.connect(self.delete_user)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)

        user_input_row = QHBoxLayout()
        user_input_row.addWidget(self.new_user_username)
        user_input_row.addWidget(self.new_user_password)
        user_input_row.addWidget(self.new_user_role)
        user_input_row.addWidget(self.create_user_button)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.selected_user_role)
        control_layout.addWidget(self.selected_user_password)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_user_button)
        button_layout.addWidget(self.delete_user_button)

        table_row_layout = QHBoxLayout()
        table_row_layout.addStretch(1)
        table_row_layout.addWidget(self.user_table)
        table_row_layout.addStretch(1)

        content = QWidget()
        content.setMinimumWidth(1600)
        content.setMaximumWidth(2400)
        content_layout = QVBoxLayout(content)
        content_layout.addLayout(header_layout)
        content_layout.addWidget(QLabel('Crear nuevo usuario (admin únicamente):'))
        content_layout.addLayout(user_input_row)
        content_layout.addSpacing(10)
        content_layout.addWidget(QLabel('Usuarios registrados:'))
        content_layout.addLayout(table_row_layout)
        content_layout.addWidget(self.selected_user_label)
        content_layout.addLayout(control_layout)
        content_layout.addLayout(button_layout)

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(content)
        layout.addStretch(1)

        self.update_permissions()

    def set_current_user(self, user_info: dict | None):
        self.current_user = user_info
        self.update_permissions()
        self.load_users()

    def update_permissions(self):
        is_admin = bool(self.current_user and self.current_user.get('role') == 'admin')
        self.new_user_username.setEnabled(is_admin)
        self.new_user_password.setEnabled(is_admin)
        self.new_user_role.setEnabled(is_admin)
        self.create_user_button.setEnabled(is_admin)
        self.user_table.setEnabled(is_admin)
        self.selected_user_role.setEnabled(is_admin)
        self.selected_user_password.setEnabled(is_admin)
        self.update_user_button.setEnabled(is_admin)
        self.delete_user_button.setEnabled(is_admin)

    def load_users(self):
        self.user_table.setRowCount(0)
        users = self.user_service.list_users()
        for row, user in enumerate(users):
            self.user_table.insertRow(row)
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.user_table.setItem(row, 2, QTableWidgetItem(user.role))

    def load_selected_user(self):
        selected = self.user_table.selectedItems()
        if not selected:
            self.selected_user_label.setText('Usuario seleccionado: Ninguno')
            self.selected_user_role.setCurrentIndex(0)
            self.selected_user_password.clear()
            return
        username = selected[1].text()
        role = selected[2].text()
        self.selected_user_label.setText(f'Usuario seleccionado: {username}')
        self.selected_user_role.setCurrentText(role)
        self.selected_user_password.clear()

    def create_user(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede crear usuarios.')
            return
        username = self.new_user_username.text().strip()
        password = self.new_user_password.text().strip()
        role = self.new_user_role.currentText()
        try:
            self.user_service.create_user(username, password, role)
            QMessageBox.information(self, 'Usuario creado', f'Usuario {username} creado con rol {role}.')
            self.new_user_username.clear()
            self.new_user_password.clear()
            self.new_user_role.setCurrentIndex(0)
            self.load_users()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def update_user(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede actualizar usuarios.')
            return
        selected = self.user_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Error', 'Seleccione un usuario para actualizar.')
            return
        user_id = int(selected[0].text())
        new_role = self.selected_user_role.currentText()
        new_password = self.selected_user_password.text().strip() or None
        try:
            self.user_service.update_user(user_id, role=new_role, password=new_password)
            QMessageBox.information(self, 'Usuario actualizado', 'El usuario ha sido actualizado correctamente.')
            self.load_users()
            self.selected_user_password.clear()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def delete_user(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede eliminar usuarios.')
            return
        selected = self.user_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Error', 'Seleccione un usuario para eliminar.')
            return
        user_id = int(selected[0].text())
        username = selected[1].text()
        if QMessageBox.question(self, 'Confirmar eliminación', f'¿Eliminar el usuario {username}?') != QMessageBox.Yes:
            return
        try:
            self.user_service.delete_user(user_id)
            QMessageBox.information(self, 'Usuario eliminado', f'Usuario {username} eliminado.')
            self.load_users()
            self.selected_user_label.setText('Usuario seleccionado: Ninguno')
            self.selected_user_password.clear()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))
