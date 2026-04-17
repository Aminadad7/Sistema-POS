from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy, QMessageBox
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
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        content = QWidget()
        content.setObjectName('loginContent')
        content.setMaximumWidth(500)
        content.setMinimumWidth(420)
        content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.addWidget(self.logo_label, alignment=Qt.AlignHCenter)
        content_layout.addWidget(title, alignment=Qt.AlignHCenter)
        content_layout.addWidget(subtitle, alignment=Qt.AlignHCenter)
        content_layout.addSpacing(16)
        content_layout.addWidget(self.username_input)
        content_layout.addWidget(self.password_input)
        content_layout.addSpacing(14)
        content_layout.addWidget(self.login_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)
        layout.addWidget(content, alignment=Qt.AlignHCenter)
        layout.addStretch(1)
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
