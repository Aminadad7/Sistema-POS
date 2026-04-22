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
    QFileDialog,
    QSizePolicy,
)
from app.utils.settings_manager import get_setting, save_settings


class SettingsView(QWidget):
    theme_changed = Signal(str)
    settings_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Configuración del Sistema')
        self.title_label.setObjectName('titleLabel')

        self.user_label = QLabel('Usuario actual: —')
        # self.info_label = QLabel('Opciones de configuración y soporte para dispositivos de impresión y lector de códigos de barras.')
        # self.info_label.setWordWrap(True)

        self.business_name_input = QLineEdit()
        self.business_name_input.setPlaceholderText('Nombre del negocio')
        self.business_address_input = QLineEdit()
        self.business_address_input.setPlaceholderText('Dirección del negocio')
        self.business_phone_input = QLineEdit()
        self.business_phone_input.setPlaceholderText('Teléfono del negocio')
        self.business_logo_input = QLineEdit()
        self.business_logo_input.setPlaceholderText('Ruta al logo del negocio')
        self.browse_logo_button = QPushButton('Seleccionar logo')
        self.browse_logo_button.clicked.connect(self.browse_logo_path)
        self.save_business_button = QPushButton('Guardar información del negocio')
        self.save_business_button.clicked.connect(self.save_business_name)

        self.theme_selector = QComboBox()
        self.theme_selector.addItem('Dark', 'dark')
        self.theme_selector.addItem('Light', 'light')
        self.theme_selector.addItem('Vino suave', 'wine')
        self.theme_selector.addItem('Vino oscuro', 'wine_dark')
        self.theme_selector.addItem('Verde oscuro', 'green_dark')
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        self.theme_selector.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.theme_selector.setMaximumWidth(180)

        content = QWidget()
        content.setObjectName('settingsContent')
        content.setMaximumWidth(1080)
        content.setMinimumWidth(840)
        content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(content)
        content_layout.addWidget(self.title_label)
        content_layout.addWidget(self.user_label)
        # content_layout.addWidget(self.info_label)
        content_layout.addSpacing(12)
        content_layout.addWidget(QLabel('Nombre del negocio:'))
        content_layout.addWidget(self.business_name_input)
        content_layout.addWidget(QLabel('Dirección del negocio:'))
        content_layout.addWidget(self.business_address_input)
        content_layout.addWidget(QLabel('Teléfono del negocio:'))
        content_layout.addWidget(self.business_phone_input)
        content_layout.addWidget(QLabel('Logo del negocio:'))
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.business_logo_input)
        logo_layout.addWidget(self.browse_logo_button)
        content_layout.addLayout(logo_layout)
        content_layout.addWidget(self.save_business_button)
        content_layout.addSpacing(12)
        content_layout.addWidget(QLabel('Tema de la aplicación:'))
        content_layout.addWidget(self.theme_selector)
        content_layout.addSpacing(8)
        content_layout.addStretch(1)

        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(content)
        layout.addStretch(1)

        self.load_business_name()
        self.update_permissions()

    def set_current_user(self, user_info: dict):
        self.current_user = user_info
        self.user_label.setText(f"Usuario actual: {user_info['username']} ({user_info['role']})")
        self.load_business_name()
        self.update_permissions()

    def load_business_name(self):
        name = get_setting('business_name') or 'Mi Negocio'
        address = get_setting('business_address') or ''
        phone = get_setting('business_phone') or ''
        theme = get_setting('theme') or 'dark'
        logo_path = get_setting('business_logo_path') or ''
        self.business_name_input.setText(name)
        self.business_address_input.setText(address)
        self.business_phone_input.setText(phone)
        self.business_logo_input.setText(logo_path)
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
        self.business_logo_input.setReadOnly(not is_admin)
        self.browse_logo_button.setEnabled(is_admin)

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
        logo_path = self.business_logo_input.text().strip()
        save_settings({
            'business_name': name,
            'business_address': address,
            'business_phone': phone,
            'business_logo_path': logo_path,
        })
        QMessageBox.information(self, 'Guardado', 'Información del negocio actualizada.')
        self.settings_updated.emit()

    def browse_logo_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Seleccionar logo del negocio',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file_path:
            self.business_logo_input.setText(file_path)
