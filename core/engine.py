import logging
from core.actions.web import WebAction
from core.actions.search import SearchAction
from core.ai_parser import GeminiParser

# Configuração de logging simples para vermos o que se passa
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class CommandEngine:
    """
    O Cérebro da aplicação.
    Agora com carregamento dinâmico de módulos (Lazy Loading) para evitar bloqueios de EDR/Antivírus.
    """
    def __init__(self):
        # Ações seguras (não interagem com o sistema operativo de baixo nível)
        self.actions = [
            WebAction(),
            SearchAction()
        ]

        # Tentamos carregar o "músculo" perigoso (PyAutoGUI) apenas se o sistema permitir
        self._load_system_actions()

        self.ai_parser = None

    def _load_system_actions(self):
        """Tenta carregar o módulo de automação de teclado de forma segura."""
        try:
            from core.actions.system import TypeAction
            self.actions.append(TypeAction())
            logging.info("Módulo de automação de sistema carregado com sucesso.")
        except ImportError:
            logging.warning("Módulo PyAutoGUI não encontrado ou bloqueado. Automação de teclado desativada.")
        except Exception as e:
            logging.error(f"Falha ao carregar automação de sistema (Provável bloqueio do EDR): {e}")

    def enable_ai(self, api_key: str):
        """Injeta a dependência da IA no motor."""
        if api_key:
             self.ai_parser = GeminiParser(api_key)
             logging.info("IA conectada com sucesso.")
        else:
             logging.warning("Nenhuma API Key fornecida. A rodar em modo básico.")

    def process(self, raw_command: str) -> dict:
        raw_command = raw_command.strip()
        if not raw_command:
            return {"status": "error", "message": "O comando fornecido está vazio."}

        # 1. Se a IA estiver ativa, traduzimos o comando primeiro!
        command_to_execute = raw_command.lower()

        if self.ai_parser:
            translated = self.ai_parser.translate_command(raw_command)

            if translated == "COMANDO_INVALIDO":
                return {"status": "error", "message": "A IA não conseguiu associar o teu pedido a uma ação conhecida."}
            elif translated.startswith("ERRO_API"):
                return {"status": "error", "message": f"Falha na IA: {translated}"}

            # Sobrescrevemos o comando bruto pela tradução limpa da IA
            command_to_execute = translated.lower()

        # 2. Busca a primeira ação que dê 'match' no comando (bruto ou traduzido)
        for action in self.actions:
            if action.match(command_to_execute):
                try:
                    # Executa a ação encapsulada
                    result_msg = action.execute(command_to_execute)

                    if self.ai_parser:
                        result_msg += f" (Traduzido pela IA de: '{raw_command}' para '{command_to_execute}')"

                    return {"status": "success", "message": result_msg}
                except Exception as e:
                    return {"status": "error", "message": f"Falha na execução da ação: {str(e)}"}

        return {"status": "error", "message": "Comando não reconhecido ou bloqueado pelo sistema."}
