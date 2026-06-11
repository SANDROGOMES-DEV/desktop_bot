from core.actions.web import WebAction
from core.actions.system import TypeAction

class CommandEngine:
    """
    O Cérebro da aplicação.
    Recebe o comando da UI, varre as estratégias registradas e executa a correta.
    """
    def __init__(self):
        # Registro de ações.
        # Para adicionar novos comandos no futuro, basta plugar a classe aqui!
        self.actions = [
            WebAction(),
            TypeAction()
        ]

    def process(self, command: str) -> dict:
        command = command.lower().strip()
        if not command:
            return {"status": "error", "message": "O comando fornecido está vazio."}

        # Busca a primeira ação que dê 'match' no comando
        for action in self.actions:
            if action.match(command):
                try:
                    # Executa a ação encapsulada
                    result_msg = action.execute(command)
                    return {"status": "success", "message": result_msg}
                except Exception as e:
                    # Fail-fast e logging de erro básico
                    return {"status": "error", "message": f"Falha na execução: {str(e)}"}

        return {"status": "error", "message": "Comando não reconhecido pelos módulos atuais."}
