from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'pos.db'
DB_URL = f'sqlite:///{DB_PATH}'
ITBIS_RATE = 0.18
BUSINESS_NAME = 'Mi Negocio'
DEFAULT_ADMIN = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'
