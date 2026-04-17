from PySide6.QtCore import Signal
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
from app.utils.settings_manager import get_setting, save_settings


class SettingsView(QWidget):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.user_service = UserService()
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Configuración del Sistema')
        self.title_label.setObjectName('titleLabel')

        self.user_label = QLabel('Usuario actual: —')
        self.info_label = QLabel('Opciones de configuración y soporte para dispositivos de impresión y lector de códigos de barras.')
        self.info_label.setWordWrap(True)

        self.business_name_input = QLineEdit()
        self.business_name_input.setPlaceholderText('Nombre del negocio')
        self.business_address_input = QLineEdit()
        self.business_address_input.setPlaceholderText('Dirección del negocio')
        self.business_phone_input = QLineEdit()
        self.business_phone_input.setPlaceholderText('Teléfono del negocio')
        self.save_business_button = QPushButton('Guardar información del negocio')
        self.save_business_button.clicked.connect(self.save_business_name)

        self.theme_selector = QComboBox()
        self.theme_selector.addItem('Dark', 'dark')
        self.theme_selector.addItem('Light', 'light')
        self.theme_selector.currentIndexChanged.connect(self.change_theme)

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
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.user_table.itemSelectionChanged.connect(self.load_selected_user)

        self.selected_user_label = QLabel('Usuario seleccionado: Ninguno')
        self.selected_user_role = QComboBox()
        self.selected_user_role.addItems(['cajero', 'admin'])
        self.selected_user_password = QLineEdit()
        self.selected_user_password.setPlaceholderText('Nueva contraseña (dejar vacío para no cambiar)')
        self.selected_user_password.setEchoMode(QLineEdit.Password)
        self.update_user_button = QPushButton('Actualizar usuario')
        self.update_user_button.clicked.connect(self.update_user)
        self.delete_user_button = QPushButton('Eliminar usuario')
        self.delete_user_button.clicked.connect(self.delete_user)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.info_label)
        layout.addSpacing(12)
        layout.addWidget(QLabel('Nombre del negocio:'))
        layout.addWidget(self.business_name_input)
        layout.addWidget(QLabel('Dirección del negocio:'))
        layout.addWidget(self.business_address_input)
        layout.addWidget(QLabel('Teléfono del negocio:'))
        layout.addWidget(self.business_phone_input)
        layout.addWidget(self.save_business_button)
        layout.addSpacing(12)
        layout.addWidget(QLabel('Tema de la aplicación:'))
        layout.addWidget(self.theme_selector)
        layout.addSpacing(12)
        layout.addWidget(QLabel('Crear nuevo usuario (admin únicamente):'))
        layout.addWidget(self.new_user_username)
        layout.addWidget(self.new_user_password)
        layout.addWidget(self.new_user_role)
        layout.addWidget(self.create_user_button)
        layout.addSpacing(20)
        layout.addWidget(QLabel('Usuarios registrados:'))
        layout.addWidget(self.user_table)
        layout.addWidget(self.selected_user_label)
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.selected_user_role)
        control_layout.addWidget(self.selected_user_password)
        layout.addLayout(control_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_user_button)
        button_layout.addWidget(self.delete_user_button)
        layout.addLayout(button_layout)
        layout.addStretch(1)

        self.load_business_name()
        self.update_permissions()

    def set_current_user(self, user_info: dict):
        self.current_user = user_info
        self.user_label.setText(f"Usuario actual: {user_info['username']} ({user_info['role']})")
        self.load_business_name()
        self.load_users()
        self.update_permissions()

    def load_business_name(self):
        name = get_setting('business_name') or 'Mi Negocio'
        address = get_setting('business_address') or ''
        phone = get_setting('business_phone') or ''
        theme = get_setting('theme') or 'dark'
        self.business_name_input.setText(name)
        self.business_address_input.setText(address)
        self.business_phone_input.setText(phone)
        index = self.theme_selector.findData(theme)
        if index >= 0:
            self.theme_selector.setCurrentIndex(index)

    def change_theme(self):
        theme = self.theme_selector.currentData()
        if theme:
            save_settings({'theme': theme})
            self.theme_changed.emit(theme)

    def update_permissions(self):
        is_admin = bool(self.current_user and self.current_user.get('role') == 'admin')
        self.business_name_input.setReadOnly(not is_admin)
        self.save_business_button.setEnabled(is_admin)
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
        user_id = int(selected[0].text())
        username = selected[1].text()
        role = selected[2].text()
        self.selected_user_label.setText(f'Usuario seleccionado: {username}')
        self.selected_user_role.setCurrentText(role)
        self.selected_user_password.clear()

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

    def save_business_name(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede cambiar la información del negocio.')
            return
        name = self.business_name_input.text().strip()
        address = self.business_address_input.text().strip()
        phone = self.business_phone_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Error', 'Ingrese un nombre válido para el negocio.')
            return
        save_settings({
            'business_name': name,
            'business_address': address,
            'business_phone': phone,
        })
        QMessageBox.information(self, 'Guardado', 'Información del negocio actualizada.')

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
