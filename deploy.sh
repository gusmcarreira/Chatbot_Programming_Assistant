# Apagar caso não seja a primeira vez
sudo rm -r Chatbot_Programming_Assistant
# Clonar o git
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
# Alterar pasta para a do Chatbot
cd Chatbot_Programming_Assistant/Chatbot
# Instalar o RASA
python3 -m pip install rasa==3.1
# Instalar outras bibliotecas necessárias
pip3 install Transformers 
pip3 install Whoosh
# A iniciar o RASA (de maneira a perimitir a integração no website) e o servidor das ações (das funções do Python)
rasa run --enable-api --cors="*" --endpoints "endpoints.yml" & rasa run actions
