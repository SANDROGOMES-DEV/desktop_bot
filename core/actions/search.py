import webbrowser
import urllib.parse
from core.actions.base import BaseAction

class SearchAction(BaseAction):
    """Lida com pesquisas automáticas no Google."""

    def match(self, command: str) -> bool:
        # Gatilhos para ativar esta ação
        triggers = ["pesquise por", "pesquisar", "busca", "buscar por", "google"]
        return any(trigger in command for trigger in triggers)

    def execute(self, command: str) -> str:
        # Removemos os gatilhos para isolar apenas o que o utilizador quer pesquisar
        termos_para_remover = ["pesquise por", "pesquisar por", "pesquisar", "busca", "buscar por", "google"]

        termo_pesquisa = command
        for termo in termos_para_remover:
            termo_pesquisa = termo_pesquisa.replace(termo, "")

        termo_pesquisa = termo_pesquisa.strip()

        if not termo_pesquisa:
            raise ValueError("Por favor, indica o que desejas pesquisar.")

        # Codifica o texto para URL (ex: "olá mundo" vira "ol%C3%A1+mundo")
        query_formatada = urllib.parse.quote_plus(termo_pesquisa)
        url = f"https://www.google.com/search?q={query_formatada}"

        webbrowser.open(url)
        return f"Pesquisa no Google iniciada para: '{termo_pesquisa}'"
