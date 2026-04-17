from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from app.services.auth_service import AuthService
from app.utils.settings_manager import get_setting


class LoginView(QWidget):
    authenticated = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_service = AuthService()
        self.setObjectName('loginView')
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(360, 320)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignCenter)

        title = QLabel('POS Sistema de Ventas')
        title.setObjectName('titleLabel')
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel('Ingrese sus credenciales para continuar')
        subtitle.setObjectName('subtitleLabel')
        subtitle.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Usuario')
        self.username_input.returnPressed.connect(self.attempt_login)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Contraseña')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.attempt_login)

        self.login_button = QPushButton('Entrar')
        self.login_button.clicked.connect(self.attempt_login)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.logo_label)
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(16)
        container_layout.addWidget(self.username_input)
        container_layout.addWidget(self.password_input)
        container_layout.addSpacing(14)
        container_layout.addWidget(self.login_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(container, alignment=Qt.AlignCenter)
        self.load_logo()

    def load_logo(self):
        logo_path = get_setting('business_logo_path') or ''
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_label.setVisible(True)
                return
        self.logo_label.clear()
        self.logo_label.setVisible(False)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            user_info = self.auth_service.login(username, password)
            self.authenticated.emit(user_info)
        except Exception as exc:
            QMessageBox.warning(self, 'Error de acceso', str(exc))
