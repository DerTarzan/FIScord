import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class ConfigError(Exception):
    pass


class BotConfigHandler:
    _instance: Optional["BotConfigHandler"] = None

    def __new__(cls, *args, **kwargs) -> "BotConfigHandler":
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.load_dotenvs()

    @staticmethod
    def load_dotenv_file(path: Path) -> None:
        if not load_dotenv(path):
            raise FileNotFoundError(f"Fehler beim Laden der Konfigurationsdatei: {path}")

    def load_dotenvs(self) -> None:
        base_dir = Path(__file__).parent / "resources"
        self.load_dotenv_file(base_dir / "config.env")
        self.load_dotenv_file(base_dir / "token.env")

class BotConfig(BotConfigHandler):
    def __init__(self):
        super().__init__()

    @property
    def TOKEN(self) -> str:
        return self._get_env_var("TOKEN")

    @property
    def STREAMS_PATH(self) -> str:
        return self._get_env_var("STREAMS_PATH")

    @property
    def WELCOME_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("WELCOME_CHANNEL_ID"))

    @property
    def BOT_CHANNEL_ID(self) -> int:
        return int(self._get_env_var("BOT_COMMANDS_CHANNEL_ID"))

    @staticmethod
    def _get_env_var(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ConfigError(f"Die Umgebungsvariable '{key}' konnte nicht geladen werden")
        return value