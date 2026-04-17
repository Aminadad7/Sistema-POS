import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget
from PySide6.QtCore import Qt
from app.ui.login_view import LoginView
from app.ui.dashboard_view import DashboardView
from app.ui.product_view import ProductView
from app.ui.client_view import ClientView
from app.ui.sales_view import SalesView
from app.ui.report_view import ReportView
from app.ui.settings_view import SettingsView
from app.ui.styles import get_theme_style
from app.utils.settings_manager import get_setting


def create_sidebar_button(text: str) -> QPushButton:
    button = QPushButton(text)
    button.setCursor(Qt.PointingHandCursor)
    button.setFixedHeight(42)
    return button


class PosMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.setWindowTitle('POS - Sistema de Punto de Venta')
        self.setMinimumSize(1200, 720)
        self.setup_ui()

    def setup_ui(self):
        self.current_theme = get_setting('theme') or 'dark'
        self.setStyleSheet(get_theme_style(self.current_theme))
        self.stack = QStackedWidget()

        self.login_view = LoginView()
        self.login_view.authenticated.connect(self.on_authenticated)
        self.stack.addWidget(self.login_view)

        self.dashboard_view = DashboardView()
        self.product_view = ProductView()
        self.client_view = ClientView()
        self.sales_view = SalesView()
        self.report_view = ReportView()
        self.settings_view = SettingsView()
        self.sales_view.sale_completed.connect(self.product_view.refresh)
        self.product_view.product_changed.connect(self.sales_view.load_products)
        self.settings_view.theme_changed.connect(self.apply_theme)

        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.product_view)
        self.stack.addWidget(self.client_view)
        self.stack.addWidget(self.sales_view)
        self.stack.addWidget(self.report_view)
        self.stack.addWidget(self.settings_view)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet('background: #111827; color: #e2e8f0; border-right: 1px solid #334155;')

        self.title_label = QLabel('POS Central')
        self.title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 12px; color: #e2e8f0;')
        self.user_label = QLabel('No logueado')
        self.user_label.setStyleSheet('color: #94a3b8; margin: 0 12px 16px;')

        self.btn_dashboard = create_sidebar_button('Dashboard')
        self.btn_products = create_sidebar_button('Productos')
        self.btn_clients = create_sidebar_button('Clientes')
        self.btn_sales = create_sidebar_button('Ventas')
        self.btn_reports = create_sidebar_button('Reportes')
        self.btn_settings = create_sidebar_button('Configuración')
        self.btn_logout = create_sidebar_button('Cerrar sesión')

        for button in [
            self.btn_dashboard,
            self.btn_products,
            self.btn_clients,
            self.btn_sales,
            self.btn_reports,
            self.btn_settings,
            self.btn_logout,
        ]:
            button.setStyleSheet(self.sidebar_button_style())

        self.btn_dashboard.clicked.connect(lambda: self.open_page(1))
        self.btn_products.clicked.connect(lambda: self.open_page(2))
        self.btn_clients.clicked.connect(lambda: self.open_page(3))
        self.btn_sales.clicked.connect(lambda: self.open_page(4))
        self.btn_reports.clicked.connect(lambda: self.open_page(5))
        self.btn_settings.clicked.connect(lambda: self.open_page(6))
        self.btn_logout.clicked.connect(self.logout)

        self.set_sidebar_enabled(False)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.addWidget(self.title_label)
        sidebar_layout.addWidget(self.user_label)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_products)
        sidebar_layout.addWidget(self.btn_clients)
        sidebar_layout.addWidget(self.btn_sales)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(self.btn_logout)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.setCentralWidget(container)
        self.open_page(0)

    def on_authenticated(self, user_info: dict):
        self.current_user = user_info
        self.user_label.setText(f"Usuario: {user_info['username']} ({user_info['role']})")
        self.dashboard_view.set_current_user(user_info)
        self.product_view.set_current_user(user_info)
        self.product_view.refresh()
        self.client_view.refresh()
        self.sales_view.set_current_user(user_info)
        self.report_view.set_current_user(user_info)
        self.report_view.refresh()
        self.settings_view.set_current_user(user_info)
        self.set_sidebar_enabled(True)
        self.apply_theme(self.current_theme)
        self.open_page(1)

    def sidebar_button_style(self):
        color = '#0f172a' if self.current_theme == 'light' else '#e2e8f0'
        return f'color: {color}; background: transparent; text-align: left; padding-left: 18px; border: none;'

    def open_page(self, index: int):
        if self.current_user is None and index != 0:
            return
        if index == 4:
            self.sales_view.load_products()
        self.stack.setCurrentIndex(index)

    def set_sidebar_enabled(self, enabled: bool):
        for button in [
            self.btn_dashboard,
            self.btn_products,
            self.btn_clients,
            self.btn_sales,
            self.btn_reports,
            self.btn_settings,
            self.btn_logout,
        ]:
            button.setEnabled(enabled)

    def apply_theme(self, theme: str):
        self.current_theme = theme
        self.setStyleSheet(get_theme_style(self.current_theme))
        if theme == 'light':
            self.sidebar.setStyleSheet('background: #e2e8f0; color: #0f172a; border-right: 1px solid #94a3b8;')
            self.title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 12px; color: #0f172a;')
            self.user_label.setStyleSheet('color: #475569; margin: 0 12px 16px;')
        else:
            self.sidebar.setStyleSheet('background: #111827; color: #e2e8f0; border-right: 1px solid #334155;')
            self.title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 12px; color: #e2e8f0;')
            self.user_label.setStyleSheet('color: #94a3b8; margin: 0 12px 16px;')
        for button in [
            self.btn_dashboard,
            self.btn_products,
            self.btn_clients,
            self.btn_sales,
            self.btn_reports,
            self.btn_settings,
            self.btn_logout,
        ]:
            button.setStyleSheet(self.sidebar_button_style())

    def logout(self):
        self.current_user = None
        self.user_label.setText('No logueado')
        self.open_page(0)


class PosApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.window = PosMainWindow()
        self.window.showMaximized()
