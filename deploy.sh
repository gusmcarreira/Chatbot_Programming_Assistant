# Apagar caso não seja a primeira vez
sudo rm -r Chatbot_Programming_Assistant
# Clonar o git
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
# Alterar pasta para a do Chatbot
cd Chatbot_Programming_Assistant/Chatbot
# Instalar o RASA
python -m pip install rasa==3.1.0
# Instalar outras bibliotecas necessárias
pip install Transformers 
pip install Whoosh
# pip install spacy
# python -m spacy download pt_core_news_md
# pip install astor
# A iniciar o RASA (de maneira a permitir a integração no website) e o servidor das ações (das funções do Python)
~/.local/bin/rasa run --enable-api --cors="*" --endpoints "endpoints.yml" --debug --log-file logs/rasa_logs.log & ~/.local/bin/rasa run actions -vv > logs/action_logs.log 2>&1 &