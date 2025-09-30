🎨 Tattoo Match

Aplicação web em Flask para agendamento de tatuagens e melhor gerenciamento do negócio.

✨ Funcionalidades

✔️ Upload de imagens de tatuagens
✔️ Galeria de imagens armazenadas
✔️ Comparação / matching de tatuagens semelhantes
✔️ Interface simples em HTML + CSS
✔️ Estrutura organizada para expansão futura

📂 Estrutura do Projeto
Tattoo_Match/
├── Templates/                  # Páginas HTML
├── static/
│   └── tattoos/                 # Imagens de tatuagens
├── instance/                    # Configurações locais
├── flask_tattoo_studio_app.py   # Aplicação principal Flask
└── README.md

⚙️ Instalação & Execução

Clone o repositório

git clone https://github.com/Allanizepi/Tattoo_Match.git
cd Tattoo_Match


Crie um ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Instale as dependências

pip install flask
pip install flask_sqlalchemy
pip install python-dotenv
pip install pandas
pip install sendgrid


Execute a aplicação

python flask_tattoo_studio_app.py


🧰 Tecnologias Utilizadas

Python 3.13.2

Flask (backend e renderização)

HTML / CSS (frontend)


🚀 Próximos Passos

🔹 Melhorar algoritmo de matching (ML/Deep Learning)
🔹 Adicionar autenticação de usuários (login/cadastro)
🔹 Criar API REST para integração com apps móveis
🔹 Interface responsiva com Bootstrap ou TailwindCSS
🔹 Deploy em servidores como Heroku, AWS ou Render


👤 Autor

Allan Izepi
📌 GitHub
