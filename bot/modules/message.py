from dataclasses import dataclass


@dataclass()
class Message:
    """Class for storage all bot text messages."""
    start: str = """Привет! Я бот для изучения армянского. Список доступных команд можно найти в /help."""