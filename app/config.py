from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'expenses.db'}"
APP_TITLE = "Expense Tracker"
APP_VERSION = "1.0.0"
DEFAULT_SORT = "date_desc"
SUPPORTED_SORTS = {"date_desc"}