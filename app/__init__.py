from app import models  # noqa: F401
from app.conf import PROJECT_ROOT, Settings

settings = Settings(_env_file=PROJECT_ROOT / ".env", _env_file_encoding="utf-8")
