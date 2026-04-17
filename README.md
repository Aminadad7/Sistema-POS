# Sistema POS en Python con PySide6

Sistema Punto de Venta modular y listo para producción construido con Python 3.11+, PySide6 y SQLAlchemy.

## Estructura del proyecto

- `app/database`: configuración de base de datos y creación de tablas.
- `app/models`: entidades del dominio.
- `app/repositories`: acceso a datos con patrón repository.
- `app/services`: lógica de negocio y validaciones.
- `app/ui`: vistas y ventanas de la aplicación.
- `app/utils`: utilidades compartidas, seguridad, logs.

## Requisitos

- Python 3.11+
- Instalar dependencias:
  ```bash
  python -m pip install -r requirements.txt
  ```

## Primer arranque

1. Crear la base de datos y usuario administrador:
   ```bash
   .venv\Scripts\python.exe run.py --init-db
   ```

2. Ejecutar la aplicación:
   ```bash
   .venv\Scripts\python.exe run.py
   ```

- En la vista de Ventas puedes generar una factura en PDF con el botón `Generar factura PDF`.
- Al finalizar la venta, la factura también se guarda automáticamente en PDF.

> Si aparece `ModuleNotFoundError` para `PySide6` u otro paquete, asegúrate de usar el intérprete dentro de `.venv`.
> También puedes ejecutar `run.bat` o `run.ps1` desde la carpeta del proyecto.

## Usuario por defecto

- Usuario: `admin`
- Contraseña: `admin123`

## Notas

- Compatible con PyInstaller.
- Preparado para migrar a PostgreSQL cambiando la URL de conexión en `app/database/session.py`.
- Interfaz con navegación lateral, teclado rápido y manejo básico de ventas.
