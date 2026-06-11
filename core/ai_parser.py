import os
import google.generativeai as genai

class GeminiParser:
    """
    Camada de inteligência artificial que traduz linguagem natural (NLP)
    para comandos estritos da nossa Engine.
    """
    def __init__(self, api_key: str = None):
        # A melhor prática: injetar a chave ou procurar no ambiente (ex: ficheiro .env)
        final_key = api_key or os.getenv("GEMINI_API_KEY")

        if not final_key:
            raise ValueError("API Key do Gemini não encontrada! Configure o ficheiro .env ou passe por parâmetro.")

        genai.configure(api_key=final_key)
        # Usamos o modelo flash por ser extremamente rápido e barato
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # O "System Prompt" é onde programamos o comportamento da IA
        self.system_prompt = """
        És o cérebro de um assistente de automação desktop.
        A tua função é ler a intenção do utilizador e traduzir para UM DOS comandos estritos abaixo.

        COMANDOS DISPONÍVEIS NO SISTEMA:
        1. Para abrir sites: 'acesse [url do site com .com ou .pt]'
        2. Para digitar texto: 'digite [texto exato]'
        3. Para pesquisar algo: 'pesquise por [termo de pesquisa]'

        REGRAS:
        - Responde APENAS com o comando traduzido. Zero conversa, zero aspas.
        - Se o utilizador pedir para abrir o "github", responde: acesse github.com
        - Se o utilizador pedir uma pesquisa complexa, responde: pesquise por [resumo da pesquisa]
        - Se for impossível mapear para as 3 ações, responde EXATAMENTE: COMANDO_INVALIDO
        """

    def translate_command(self, user_input: str) -> str:
        try:
            prompt_completo = f"{self.system_prompt}\n\nComando do utilizador: {user_input}"
            response = self.model.generate_content(prompt_completo)
            comando_traduzido = response.text.strip()
            return comando_traduzido
        except Exception as e:
            # Em caso de falha de rede ou chave inválida, avisa a Engine
            return f"ERRO_API: {str(e)}"
