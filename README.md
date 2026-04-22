# Sistema POS en Python con PySide6

Aplicación de Punto de Venta (POS) construida con Python 3.11+, PySide6 y SQLAlchemy. Incluye inventario, clientes, ventas, reportes, facturación en PDF y soporte de temas claros/oscuro.

## Características principales

- Gestión de productos, clientes y ventas.
- Panel de control con estadísticas de ventas, clientes y productos.
- Múltiples reportes: ventas de hoy, ventas por mes, ventas históricas.
- Generación de facturas en PDF, incluyendo logo, datos del negocio y resumen de totales.
- Soporte para tema `dark` y `light` con contraste mejorado en modo claro.
- Configuración de negocio desde la UI: nombre, dirección, teléfono y logo.
- Usuarios con permisos `admin` y `cajero`, control de creación/actualización de usuarios.

## Estructura del proyecto

- `app/database`: configuración de base de datos, sesión y migraciones.
- `app/models`: entidades del dominio del POS.
- `app/repositories`: acceso a datos con patrón repository.
- `app/services`: lógica de negocio, validaciones y reportes.
- `app/ui`: vistas, ventanas y controles de la interfaz.
- `app/utils`: utilidades compartidas, settings, PDF y constantes.

## Requisitos

- Python 3.11 o superior
- Dependencias del proyecto:
  ```bash
  python -m pip install -r requirements.txt
  ```

## Arranque rápido

1. Inicializa la base de datos y crea el administrador:
   ```bash
   .venv\Scripts\python.exe run.py --init-db
   ```

2. Inicia la aplicación:
   ```bash
   .venv\Scripts\python.exe run.py
   ```

> Si usas PowerShell, puedes ejecutar `.
un.ps1` si existe el script de arranque.

## Uso básico

- `Login`: ingresar con credenciales válidas para activar la navegación.
- `Dashboard`: ver estadísticas clave y tablas con encabezados claros.
- `Productos`: administrar inventario.
- `Clientes`: administrar clientes registrados.
- `Ventas`: agregar productos al carrito, aplicar descuentos, seleccionar cliente y generar factura en PDF.
- `Reportes`: descargar facturas históricas y revisar resúmenes por periodo.
- `Configuración`: cambiar tema, editar datos del negocio y cargar el logo para mostrarlo en la UI y facturas.

## Configuración de logo y brand

En `Configuración del Sistema` puedes:

- Guardar nombre del negocio.
- Guardar dirección y teléfono del negocio.
- Seleccionar un archivo de logo para usar en:
  - pantalla de login
  - encabezado del dashboard
  - barra lateral principal
  - facturas PDF generadas

## Generación de facturas PDF

- Las facturas se generan desde la vista de `Ventas` con el botón `Generar factura PDF`.
- También se generan automáticamente al finalizar una venta.
- El PDF incluye:
  - logo configurado (si existe)
  - datos del negocio
  - número de factura, fecha y cliente
  - lista de productos, cantidad, precios y totales
  - resumen de subtotal, descuento, ITBIS, total, pagado y cambio

## Usuario por defecto

- Usuario: `admin`
- Contraseña: **consultar configuración o generar usuario administrativo en la inicialización**

## Notas adicionales

- Compatible con PyInstaller y empaquetado distributivo.
- Preparado para migrar a PostgreSQL cambiando la configuración de conexión en `app/database/session.py`.
- Recomendado ejecutar desde el entorno virtual `.venv` para evitar conflictos de dependencias.
- Si ves un error `ModuleNotFoundError`, asegúrate de activar el ambiente virtual antes de ejecutar la aplicación.

## Instalador tipo wizard (Windows)

Para generar un instalador con asistente (pantallas de "Siguiente") se usa Inno Setup.

1. Instala Inno Setup 6 (debe existir `ISCC.exe`).
2. Ejecuta:
  ```powershell
  .\build_installer.ps1
  ```

Este script:

- Genera el ejecutable con PyInstaller en `dist_installer/run`.
- Compila el instalador usando `installer/SistemaPOS.iss`.
- Deja el instalador en `installer/output/SistemaPOS-Setup.exe`.

## Más información

- `app/ui/main_window.py`: control principal de navegación y aplicación de temas.
- `app/ui/settings_view.py`: ajustes del negocio y selección de logo.
- `app/utils/pdf_generator.py`: generación de facturas en PDF con logo.
- `app/services/report_service.py`: construye datos para reportes y exportación de facturas.
