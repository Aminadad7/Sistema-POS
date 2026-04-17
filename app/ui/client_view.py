from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QSizePolicy,
    QHeaderView,
)
from app.services.client_service import ClientService
from app.repositories.client_repository import ClientRepository


class ClientView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.client_service = ClientService()
        self.client_repository = ClientRepository()
        self.selected_client_id = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Gestión de Clientes')
        self.title_label.setObjectName('titleLabel')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Nombre')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Teléfono')
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText('Dirección')

        self.save_button = QPushButton('Guardar')
        self.save_button.clicked.connect(self.save_client)
        self.delete_button = QPushButton('Eliminar selección')
        self.delete_button.clicked.connect(self.delete_client)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.address_input)
        form_layout.addWidget(self.save_button)
        form_layout.addWidget(self.delete_button)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Email', 'Teléfono', 'Dirección'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumHeight(350)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.itemSelectionChanged.connect(self.load_selection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        clients = self.client_service.list_clients()
        for row, client in enumerate(clients):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(client.id)))
            self.table.setItem(row, 1, QTableWidgetItem(client.name))
            self.table.setItem(row, 2, QTableWidgetItem(client.email or ''))
            self.table.setItem(row, 3, QTableWidgetItem(client.phone or ''))
            self.table.setItem(row, 4, QTableWidgetItem(client.address or ''))

    def load_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            self.selected_client_id = None
            return
        self.selected_client_id = int(selected[0].text())
        client = self.client_repository.get_by_id(self.selected_client_id)
        if client:
            self.name_input.setText(client.name)
            self.email_input.setText(client.email or '')
            self.phone_input.setText(client.phone or '')
            self.address_input.setText(client.address or '')

    def save_client(self):
        try:
            name = self.name_input.text()
            email = self.email_input.text()
            phone = self.phone_input.text()
            address = self.address_input.text()
            if self.selected_client_id:
                client = self.client_repository.get_by_id(self.selected_client_id)
                if not client:
                    raise ValueError('Cliente no encontrado.')
                self.client_service.update_client(client, name, email, phone, address)
            else:
                self.client_service.create_client(name, email, phone, address)
            QMessageBox.information(self, 'Éxito', 'Cliente guardado correctamente.')
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def delete_client(self):
        if not self.selected_client_id:
            QMessageBox.warning(self, 'Error', 'Seleccione un cliente para eliminar.')
            return
        client = self.client_repository.get_by_id(self.selected_client_id)
        if not client:
            QMessageBox.warning(self, 'Error', 'Cliente no encontrado.')
            return
        try:
            self.client_service.delete_client(client)
            QMessageBox.information(self, 'Éxito', 'Cliente eliminado.')
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def clear_form(self):
        self.selected_client_id = None
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
