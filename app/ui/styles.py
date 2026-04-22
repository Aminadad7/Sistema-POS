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
    padding: 12px;
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
    padding: 12px;
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

wine_style = """
QMainWindow {
    background: #2b1a21;
}
QWidget {
    background: transparent;
    color: #f6ebef;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 12pt;
}
QPushButton {
    background: #8b3f5e;
    color: #fff7fa;
    border-radius: 6px;
    padding: 8px 14px;
}
QPushButton:hover {
    background: #9c4d6d;
}
QPushButton:disabled {
    background: #6b4a58;
    color: #dbc3cd;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background: #3a2530;
    border: 1px solid #785161;
    border-radius: 8px;
    padding: 10px;
    color: #f6ebef;
}
QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    min-height: 36px;
}
QLabel {
    color: #f6ebef;
}
QTableWidget {
    background: #3a2530;
    alternate-background-color: #432b37;
    border: 1px solid #785161;
    color: #f6ebef;
}
QTableWidget::item {
    color: #f6ebef;
}
QTableWidget::item:selected {
    background: #8b3f5e;
    color: #fff7fa;
}
QHeaderView::section {
    background: #533442;
    color: #f6ebef;
    padding: 12px;
    border: 1px solid #785161;
}
QFrame {
    background: transparent;
    color: #f6ebef;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #fff7fa;
}
QLabel#subtitleLabel {
    font-size: 14px;
    color: #d9bcc8;
}
QMessageBox, QMessageBox QLabel, QMessageBox QPushButton {
    background: #3a2530;
    color: #f6ebef;
}
QMessageBox QPushButton {
    background: #6d4656;
    border-radius: 6px;
    padding: 6px 12px;
}
QMessageBox QPushButton:hover {
    background: #7f5366;
}
"""

wine_dark_style = """
QMainWindow {
    background: #1f1217;
}
QWidget {
    background: transparent;
    color: #f7edf1;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 12pt;
}
QPushButton {
    background: #6f2f47;
    color: #fff7fa;
    border-radius: 6px;
    padding: 8px 14px;
}
QPushButton:hover {
    background: #813853;
}
QPushButton:disabled {
    background: #5a3d49;
    color: #cfb7c2;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background: #2b1a21;
    border: 1px solid #5f3b4a;
    border-radius: 8px;
    padding: 10px;
    color: #f7edf1;
}
QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    min-height: 36px;
}
QLabel {
    color: #f7edf1;
}
QTableWidget {
    background: #2b1a21;
    alternate-background-color: #322029;
    border: 1px solid #5f3b4a;
    color: #f7edf1;
}
QTableWidget::item {
    color: #f7edf1;
}
QTableWidget::item:selected {
    background: #6f2f47;
    color: #fff7fa;
}
QHeaderView::section {
    background: #3e2732;
    color: #f7edf1;
    padding: 12px;
    border: 1px solid #5f3b4a;
}
QFrame {
    background: transparent;
    color: #f7edf1;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #fff7fa;
}
QLabel#subtitleLabel {
    font-size: 14px;
    color: #d8bcc7;
}
QMessageBox, QMessageBox QLabel, QMessageBox QPushButton {
    background: #2b1a21;
    color: #f7edf1;
}
QMessageBox QPushButton {
    background: #553542;
    border-radius: 6px;
    padding: 6px 12px;
}
QMessageBox QPushButton:hover {
    background: #664250;
}
"""

green_dark_style = """
QMainWindow {
    background: #0f1b17;
}
QWidget {
    background: transparent;
    color: #e9f5ef;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 12pt;
}
QPushButton {
    background: #2f6b55;
    color: #f3fffa;
    border-radius: 6px;
    padding: 8px 14px;
}
QPushButton:hover {
    background: #397a63;
}
QPushButton:disabled {
    background: #415b51;
    color: #b9d3c8;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background: #152520;
    border: 1px solid #3e6757;
    border-radius: 8px;
    padding: 10px;
    color: #e9f5ef;
}
QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    min-height: 36px;
}
QLabel {
    color: #e9f5ef;
}
QTableWidget {
    background: #152520;
    alternate-background-color: #1a2d27;
    border: 1px solid #3e6757;
    color: #e9f5ef;
}
QTableWidget::item {
    color: #e9f5ef;
}
QTableWidget::item:selected {
    background: #2f6b55;
    color: #f3fffa;
}
QHeaderView::section {
    background: #243a33;
    color: #e9f5ef;
    padding: 12px;
    border: 1px solid #3e6757;
}
QFrame {
    background: transparent;
    color: #e9f5ef;
}
QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #f3fffa;
}
QLabel#subtitleLabel {
    font-size: 14px;
    color: #bad7ca;
}
QMessageBox, QMessageBox QLabel, QMessageBox QPushButton {
    background: #152520;
    color: #e9f5ef;
}
QMessageBox QPushButton {
    background: #335447;
    border-radius: 6px;
    padding: 6px 12px;
}
QMessageBox QPushButton:hover {
    background: #3c6253;
}
"""


def get_theme_style(theme: str = 'dark') -> str:
    if theme == 'light':
        return light_style
    if theme == 'wine_dark':
        return wine_dark_style
    if theme == 'green_dark':
        return green_dark_style
    if theme == 'wine':
        return wine_style
    return dark_style
