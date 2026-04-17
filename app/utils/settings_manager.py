import json
from pathlib import Path
from app.utils.constants import BASE_DIR, BUSINESS_NAME

SETTINGS_FILE = BASE_DIR / 'settings.json'
DEFAULT_SETTINGS = {
    'business_name': BUSINESS_NAME,
    'business_address': '',
    'business_phone': '',
    'business_logo_path': '',
    'theme': 'dark',
}


def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()
    try:
        with SETTINGS_FILE.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
    except Exception:
        return DEFAULT_SETTINGS.copy()
    return {**DEFAULT_SETTINGS, **data}


def save_settings(settings: dict) -> dict:
    current = load_settings()
    current.update(settings)
    with SETTINGS_FILE.open('w', encoding='utf-8') as handle:
        json.dump(current, handle, indent=2, ensure_ascii=False)
    return current


def get_setting(key: str):
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))
