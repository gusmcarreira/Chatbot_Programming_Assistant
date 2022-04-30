# Apagar caso não seja a primeira vez
sudo rm -r Chatbot_Programming_Assistant
# Clonar o git
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
# Alterar pasta para a do Chatbot
cd Chatbot_Programming_Assistant/Chatbot
# Criar ambiente virtual
python3 -m venv venv
# Instalar o RASA
venv/bin/python3 -m pip install rasa
# Instalar outras bibliotecas necessárias
venv/bin/pip3 install Transformers 
venv/bin/pip3 install Whoosh
# A iniciar o RASA (de maneira a perimitir a integração no website) e o servidor das ações (das funções do Python)
venv/bin/rasa run --enable-api --cors="*" --endpoints "endpoints.yml" --debug --log-file logs/rasa_logs.log & venv/bin/rasa run actions -vv > logs/action_logs.log 2>&1
