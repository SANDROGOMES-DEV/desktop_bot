import pyautogui
import time
from core.actions.base import BaseAction

class TypeAction(BaseAction):
    """Lida com automação de teclado usando PyAutoGUI."""

    def match(self, command: str) -> bool:
        return "digite" in command

    def execute(self, command: str) -> str:
        # Extrai o texto a ser digitado
        texto = command.replace("digite", "").strip()

        # Pausa bloqueante controlada (apenas na thread de execução da ação)
        time.sleep(3)

        # Typing humanizado (intervalo de 0.05s entre teclas)
        pyautogui.write(texto, interval=0.05)

        return f"Texto '{texto}' injetado via teclado com sucesso."
