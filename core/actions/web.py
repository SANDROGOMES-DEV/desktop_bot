import webbrowser
from core.actions.base import BaseAction

class WebAction(BaseAction):
    """Lida com abertura de URLs e navegação web."""

    def match(self, command: str) -> bool:
        # Gatilhos mais curtos e diretos
        triggers = ["acesse", "abrir", "navegar", "abra", "site"]
        return any(trigger in command for trigger in triggers)

    def execute(self, command: str) -> str:
        words = command.split()
        url = words[-1] # Pega a última palavra assumindo ser a URL

        # Sanitização básica de input
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        webbrowser.open(url)
        return f"Navegador acionado para a URL: {url}"
