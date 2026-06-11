from abc import ABC, abstractmethod

class BaseAction(ABC):
    """
    Contrato base para qualquer ação do bot.
    Garante que todas as ações tenham o mesmo comportamento público.
    """

    @abstractmethod
    def match(self, command: str) -> bool:
        """Verifica se esta ação deve ser ativada pelo comando."""
        pass

    @abstractmethod
    def execute(self, command: str) -> str:
        """Executa a ação e retorna uma mensagem de status."""
        pass
