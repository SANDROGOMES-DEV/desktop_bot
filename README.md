⚙️ Automator Engine v2.0

Um assistente de automação desktop modular e escalável, construído com Python e Streamlit.

Este projeto foi refatorado utilizando princípios de Engenharia de Software (S.O.L.I.D, Design Patterns como Strategy/Command) para separar a interface de usuário (UI) da lógica de negócios e execução de tarefas.

📁 Estrutura da Arquitetura

desktop_bot/
├── app.py                # Interface Streamlit (View)
├── requirements.txt      # Dependências do projeto
├── .gitignore            # Regras de exclusão do Git
└── core/                 # Domínio e Lógica de Negócios
    ├── __init__.py
    ├── engine.py         # Orquestrador de comandos (Controller)
    └── actions/          # Módulos de ação independentes
        ├── __init__.py
        ├── base.py       # Interface/Contrato Base
        ├── web.py        # Automação de Navegador
        └── system.py     # Automação de Teclado/Mouse


🚀 Como Executar Localmente

1. Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado em sua máquina.

2. Instalação

Clone o repositório e entre na pasta:

git clone [https://github.com/SEU_USUARIO/automator-engine.git](https://github.com/SEU_USUARIO/automator-engine.git)
cd automator-engine


Crie e ative um ambiente virtual (Recomendado):

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate


Instale as dependências:

pip install -r requirements.txt


3. Execução

Com o ambiente ativado, rode a interface do Streamlit:

streamlit run app.py


O sistema abrirá automaticamente no seu navegador padrão em http://localhost:8501.

🛠️ Como Adicionar Novos Comandos

Graças à arquitetura modular, para adicionar uma nova funcionalidade (ex: ler PDFs, enviar e-mails), você não precisa modificar o app.py.

Crie um novo arquivo em core/actions/ (ex: email.py).

Crie uma classe que herde de BaseAction e implemente os métodos match() e execute().

Registre a sua nova classe na lista de ações dentro de core/engine.py.