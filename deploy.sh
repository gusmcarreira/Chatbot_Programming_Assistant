# Apagar caso não seja a primeira vez
rm -r Chatbot_Programming_Assistant
# Clonar o git
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
# Alterar pasta para a do Chatbot
cd Chatbot_Programming_Assistant/Chatbot
# Instalar o RASA
python -m pip install rasa
# Instalar outras bibliotecas necessárias
pip install Transformers && pip install Whoosh
# A iniciar o RASA (de maneira a perimitir a integração no website) e o servidor das ações (das funções do Python)
rasa run --enable-api --cors="*" --endpoints "endpoints.yml" && rasa run actions