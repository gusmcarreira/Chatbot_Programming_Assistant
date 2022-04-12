# Apagar caso não seja a primeira vez
sudo rm -r Chatbot_Programming_Assistant
# Clonar o git
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
# Alterar pasta para a do Chatbot
cd Chatbot_Programming_Assistant/Chatbot
# Criar ambiente virtual
python -m venv venv
# Instalar o RASA
venv/bin/python -m pip install rasa==3.1
# Instalar outras bibliotecas necessárias
venv/bin/pip install Transformers && venv/bin/pip install Whoosh
# A iniciar o RASA (de maneira a perimitir a integração no website) e o servidor das ações (das funções do Python)
venv/bin/rasa run --enable-api --cors="*" --endpoints "endpoints.yml" & venv/bin/rasa run actions