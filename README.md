# Chatbot_Programming_Assistant

## Chatbot Widget
Ver em:
* https://github.com/gusmcarreira/Chatbot_Front_End

## Perguntas feitas consoante o erro
###Estrutura:
* __Pergunta:__ (Obrigatório) Respetiva pergunta
* __Resposta:__ (Obrigatório) Respetiva resposta
* __Opções Iniciais:__ (Opcional) Opções a mostrar independentemente se o aluno sabe/não sabe a resposata
* __Opções:__ (Opcional) Opções que são apenas mostradas se o aluno disser que não sabe, ou se responder de forma incorreta
* __Explicação:__ (Opcional) Explicação que será mostrada caso o aluno dê a resposta incorreta
* __-#-__ (Obrigatório)
  * Separa os blocos de informações de cada pergunta
  * Também separa as perguntas do checkpoint
* __Checkpoint:__ (Obrigatório) Resumo do guia (simboliza o final da ajuda)

###Organização:
* A localização dos ficheiros, consoante o tópico (Função, Repetição, Condição, Variável), pode ser encontrado nos ficheiros dos mesmos nomes em:
    * Chatbot/actions/custom/Docs/ErrorGuidance/ ou https://github.com/gusmcarreira/Chatbot_Programming_Assistant/tree/main/Chatbot/actions/custom/Docs/ErrorGuidance
        * ErrorGuidance/Condição.txt
        * ErrorGuidance/Função.txt
        * ErrorGuidance/Repetição.txt
        * ErrorGuidance/Variável.txt
      
* Ter em atenção que o tópico do erro deve coincidir exatamente com o título dos ficheiros e pastas em ErrorGuidance/, tal como o erro dado tem de coincidir exatamente com as mensagens nos 4 ficheiros mencionados atrás.
* As perguntas elaboradas para cada erro econtram-se dentro de cada uma das pastas respetivas ao tópico em questão, dentro das pasta ErrorGuidance/
        * ErrorGuidance/Condição/...txt
        * ErrorGuidance/Função/...txt
        * ErrorGuidance/Repetição/...txt
        * ErrorGuidance/Variável/...txt

## Instalação
### Manual:
* Instalar Rasa
```
python -m pip install rasa
```

* Instalar outras libraries:
```
pip install Transformers
pip install Whoosh
```
* Clonar o git
```
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
```
* Mudar para a pasta do Chatbot
```
cd Chatbot
```
* Verificar que o url do action_endpoint corresponde ao seguinte
```
action_endpoint:
  url: "http://localhost:5055/webhook"
```
* Treinar Modelo
```
rasa train
```
* Correr o RASA de maneira a permitir integração em website
```
rasa run --enable-api --cors="*"
```
* Correr também o servidos das ações
```
rasa run actions
```
###Com docker-compose:
* Clonar o git
```
git clone https://github.com/gusmcarreira/Chatbot_Programming_Assistant.git
```
* Mudar para pasta:
```
cd Chatbot
```
* Verificar que o url do action_endpoint corresponde ao seguinte
```
action_endpoint:
  url: "http://app:5055/webhook"
```
* Correr o docker-compose
```
docker-compose up
```

##Problemas/TODO:
* Está a dar erro quando se pede exemplo/definição devido ao modelo de resposta automática (docker-compose)
* Guião de perguntas (na resoulução de problemas) deve ser melhorado
* Estilo das mensagens (deve ser melhorado, principalmete do quando o display é código)
* Erros lógicos...
