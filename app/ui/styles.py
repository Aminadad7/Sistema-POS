dark_style = """
QMainWindow {
    background: #0f172a;
}
QWidget {
    background: transparent;
    color: #e2e8f0;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 12pt;
}
QPushButton {
    background: #2563eb;
    color: white;
    border-radius: 6px;
    padding: 8px 14px;
}
QPushButton:hover {
    background: #1d4ed8;
}
QPushButton:disabled {
    background: #475569;
    color: #cbd5e1;
}
QLineEdit, QComboBox, QSpinBox {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    color: #e2e8f0;
}
QComboBox, QSpinBox {
    min-height: 32px;
}
QLabel {
    color: #e2e8f0;
}
QTableWidget {
    background: #111827;
    border: 1px solid #334155;
    color: #e2e8f0;
}
QTableWidget::item {
    color: #e2e8f0;
}
QTableWidget::item:selected {
    background: #2563eb;
    color: white;
}
QHeaderView::section {
    background: #1e293b;
    color: #e2e8f0;
    padding: 8px;
    border: 1px solid #334155;
}
QFrame {
    background: transparent;
    color: #e2e8f0;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #f8fafc;
}
QLabel#subtitleLabel {
    font-size: 14px;
    color: #94a3b8;
}
QMessageBox, QMessageBox QLabel, QMessageBox QPushButton {
    background: #111827;
    color: #e2e8f0;
}
QMessageBox QPushButton {
    background: #334155;
    border-radius: 6px;
    padding: 6px 12px;
}
QMessageBox QPushButton:hover {
    background: #475569;
}
"""

light_style = """
QMainWindow {
    background: #f3f4f6;
}
QWidget, QFrame, QStackedWidget {
    background: #f3f4f6;
    color: #111827;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 12pt;
}
QPushButton {
    background: #2563eb;
    color: white;
    border-radius: 6px;
    padding: 8px 14px;
}
QPushButton:hover {
    background: #1d4ed8;
}
QPushButton:disabled {
    background: #cbd5e1;
    color: #475569;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px;
    color: #111827;
}
QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    min-height: 36px;
}
QLabel {
    color: #111827;
}
QTableWidget {
    background: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    color: #111827;
}
QTableWidget::item {
    color: #111827;
}
QTableWidget::item:selected {
    background: #2563eb;
    color: white;
}
QHeaderView::section {
    background: #e2e8f0;
    color: #111827;
    padding: 8px;
    border: 1px solid #cbd5e1;
}
QFrame {
    background: #f3f4f6;
    color: #111827;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #111827;
}
QLabel#subtitleLabel {
    font-size: 14px;
    color: #1f2937;
}
QMessageBox, QMessageBox QLabel, QMessageBox QPushButton {
    background: #ffffff;
    color: #111827;
}
QMessageBox QPushButton {
    background: #e2e8f0;
    border-radius: 6px;
    padding: 6px 12px;
}
QMessageBox QPushButton:hover {
    background: #cbd5e1;
}
"""


def get_theme_style(theme: str = 'dark') -> str:
    return dark_style if theme == 'dark' else light_style
