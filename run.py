import sys
import argparse

try:
    from app.database.init_db import initialize_database
except ImportError as exc:
    print('Error al importar los módulos de base de datos:')
    print(exc)
    print('\nAsegúrate de ejecutar el proyecto con el entorno virtual del proyecto (.venv).')
    print('Ejemplo: .venv\\Scripts\\python.exe run.py --init-db')
    sys.exit(1)


def main():
    try:
        from app.ui.main_window import PosApplication
    except ImportError as exc:
        print('Error al iniciar la interfaz gráfica:')
        print(exc)
        print('\nAsegúrate de ejecutar el proyecto con el entorno virtual del proyecto (.venv).')
        print('Ejemplo: .venv\\Scripts\\python.exe run.py')
        sys.exit(1)
    parser = argparse.ArgumentParser(description='POS System Launcher')
    parser.add_argument('--init-db', action='store_true', help='Initialize database and create default admin user')
    args = parser.parse_args()

    if args.init_db:
        initialize_database()
        print('Base de datos inicializada con el usuario admin/admin123.')
        return

    initialize_database()
    app = PosApplication(sys.argv)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


